import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.test()
async def test_file(dut):
    for i in range (800 * 525):
        dut.x_pos.value = i % 800
        dut.y_pos.value = i // 800

        await Timer(1, unit="ns")

        x_pos = i % 800
        y_pos = i // 800

        c_x = x_pos * round(3.5 / 639 * 32768) - 2.5 * 32768
        c_y = y_pos * round(2 / 479 * 32768) - 1 * 32768

        assert c_x == dut.c_x.value.to_signed(), f"Expected c_x={c_x}, got c_x={dut.c_x.value.to_signed()}"
        assert c_y == dut.c_y.value.to_signed(), f"Expected c_y={c_y}, got c_y={dut.c_y.value.to_signed()}"     