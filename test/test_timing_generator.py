import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

async def reset_dut(dut):
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

@cocotb.test()
async def test_timing_generator(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    for i in range(800 * 525):

        await FallingEdge(dut.clk)
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

        await ClockCycles(dut.clk, 1)
