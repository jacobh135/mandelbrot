import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def reset_dut(dut):
    dut.rst_n.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

@cocotb.test()
async def test_timing_generator(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    assert dut.x_t.value.to_signed() == -32, f"Expected x_t={-32}, got x_t={dut.x_t.value.to_signed()}"
    assert dut.y_t.value.to_signed() == 0, f"Expected y_t={0}, got y_t={dut.y_t.value.to_signed()}"

    assert dut.hsync.value == 1, f"Expected hsync={1}, got hsync={dut.hsync.value}"
    assert dut.vsync.value == 1, f"Expected vsync={1}, got vsync={dut.vsync.value}"
    assert dut.video_active.value == 0, f"Expected video_active={0}, got video_active={dut.video_active.value}"

    dut.enable.value = 1

    for i in range(800 * 525):

        await FallingEdge(dut.clk)

        x_t = i % 800
        y_t = i // 800
        assert dut.x_t.value.to_signed() == x_t, f"Expected x_t={x_t}, got x_t={dut.x_t.value.to_signed()}"
        assert dut.y_t.value.to_signed() == y_t, f"Expected y_t={y_t}, got y_t={dut.y_t.value.to_signed()}"

        hsync = int(not ((656 <= x_t) and (751 >= x_t)))
        vsync = int(not ((490 <= y_t) and (491 >= y_t)))
        video_active = int((639 >= x_t) and (479 >= y_t))
        assert dut.hsync.value == hsync, f"Expected hsync={hsync}, got hsync={dut.hsync.value}"
        assert dut.vsync.value == vsync, f"Expected vsync={vsync}, got vsync={dut.vsync.value}"
        assert dut.video_active.value == video_active, f"Expected video_active={video_active}, got video_active={dut.video_active.value}"
