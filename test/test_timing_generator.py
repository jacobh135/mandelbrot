import cocotb
from cocotb.clock import Clock
from cocotb.triggers import NextTimeStep, RisingEdge, ReadOnly

async def reset_dut(dut):
    dut.rst_b.value = 0
    await RisingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_timing_generator(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    for i in range(800 * 525):

        await ReadOnly()
        x_pos = i % 800
        y_pos = i // 800
        assert x_pos == dut.x_pos.value, f"Expected x_pos={x_pos}, got x_pos={dut.x_pos.value}"
        assert y_pos == dut.y_pos.value, f"Expected y_pos={y_pos}, got y_pos={dut.y_pos.value}"

        hsync = int(not ((656 <= x_pos) and (751 >= x_pos)))
        vsync = int(not ((490 <= y_pos) and (491 >= y_pos)))
        video_active = int((639 >= x_pos) and (479 >= y_pos))
        assert hsync == dut.hsync.value, f"Expected hsync={hsync}, got hsync={dut.hsync.value}"
        assert vsync == dut.vsync.value, f"Expected vsync={vsync}, got vsync={dut.vsync.value}"
        assert video_active == dut.video_active.value, f"Expected video_active={video_active}, got video_active={dut.video_active.value}"

        await RisingEdge(dut.clk)
