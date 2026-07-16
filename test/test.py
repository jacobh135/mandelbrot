# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ReadOnly


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # # Set the input values you want to test
    # dut.ui_in.value = 20
    # dut.uio_in.value = 30

    # # Wait for one clock cycle to see the output values
    # await ClockCycles(dut.clk, 1)

    # # The following assersion is just an example of how to check the output values.
    # # Change it to match the actual expected output of your module:
    # assert dut.uo_out.value == 50

    # # Keep testing the module by changing the input values, waiting for
    # # one or more clock cycles, and asserting the expected output values.

    for i in range(800 * 525):
        await ReadOnly()
        uo_out = 0

        x_pos = i % 800
        y_pos = i // 800

        hsync = int(not ((656 <= x_pos) and (751 >= x_pos)))
        vsync = int(not ((490 <= y_pos) and (491 >= y_pos)))
        video_active = int((639 >= x_pos) and (479 >= y_pos))

        if (video_active):
            red = (x_pos // 128) % 2
            green = (x_pos // 64) % 2
            blue = (x_pos // 32) % 2
        else:
            red = 0
            green = 0
            blue = 0

        if (red):
            uo_out += 1 + 16
        if (green):
            uo_out += 2 + 32
        if (blue):
            uo_out += 4 + 64
        if (hsync):
            uo_out += 128
        if (vsync):
            uo_out += 8

        assert uo_out == dut.uo_out.value

        await ClockCycles(dut.clk, 1)