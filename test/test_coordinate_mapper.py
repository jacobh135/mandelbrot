import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.test()
async def test_coordinate_mapper(dut):

    frac = int(os.environ.get("FRAC", "12"))

    for i in range (800 * 525):
        dut.x_pos.value = i % 800
        dut.y_pos.value = i // 800

        await Timer(1, unit="ns")

        x_pos = i % 800
        y_pos = i // 800

        x_scale = (7 * (1 << (frac - 1)) + 319) // 639
        y_scale = ((1 << (frac + 1)) + 239) // 479
        x_off   = 5 << (frac - 1)
        y_off   = 1 << frac

        c_x = x_pos * x_scale - x_off
        c_y = y_pos * y_scale - y_off

        assert c_x == dut.c_x.value.to_signed(), f"Expected c_x={c_x}, got c_x={dut.c_x.value.to_signed()}"
        assert c_y == dut.c_y.value.to_signed(), f"Expected c_y={c_y}, got c_y={dut.c_y.value.to_signed()}"     