import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_video_on(dut):
    dut.red.value = 2;
    dut.green.value = 1;
    dut.blue.value = 3;
    dut.hsync.value = 0;
    dut.vsync.value = 0;
    dut.video_active.value = 1;

    await Timer(1, unit="ns")
    assert dut.uo_out.value == 101, f"Expected uo_out=101, got uo_out={dut.uo_out.value}"

@cocotb.test()
async def test_video_off(dut):
    dut.red.value = 3;
    dut.green.value = 2;
    dut.blue.value = 2;
    dut.hsync.value = 1;
    dut.vsync.value = 0;
    dut.video_active.value = 0;

    await Timer(1, unit="ns")
    assert dut.uo_out.value == 128, f"Expected uo_out=128, got uo_out={dut.uo_out.value}"
