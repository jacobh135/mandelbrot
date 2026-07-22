# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

def adjust(num, frac):
    num %= (2 ** (frac + 3))
    if (num >= (2 ** (frac + 2))):
        num -= (2 ** (frac + 3))

    return num

def find_count(c_x, c_y, frac):
    z_x = 0
    z_y = 0
    count = 0
    while ((z_x ** 2 + z_y ** 2 <= 4 * (2 ** frac) ** 2) and (count < 24)):
        z_x_new = adjust((z_x ** 2) // (2 ** frac) - (z_y ** 2) // (2 ** frac) + c_x, frac)
        z_y_new = adjust(2 * ((z_x * z_y) // (2 ** frac)) + c_y, frac)
        z_x = z_x_new
        z_y = z_y_new
        count += 1
    return count

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="ns") # ns
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

    colors = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 0, 2],
        [1, 0, 3],
        [0, 0, 3],
        [0, 1, 3],
        [0, 1, 2],
        [0, 2, 3],
        [0, 2, 2],
        [0, 3, 3],
        [1, 3, 3],
        [1, 3, 2],
        [1, 3, 1],
        [2, 3, 1],
        [2, 3, 0],
        [3, 3, 0],
        [3, 2, 0],
        [2, 2, 0],
        [3, 1, 0],
        [2, 1, 0],
        [3, 0, 0],
        [3, 0, 1],
        [2, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    frac = int(os.environ.get("FRAC"))

    while (dut.user_project.cranker_done.value == 0):
        await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)

    for i in range(800 * 525):
        x_t = i % 800
        y_t = i // 800

        x_pos = (x_t // 32) * 32
        y_pos = (y_t // 32) * 32

        x_scale = (7 * (1 << (frac - 1)) + 319) // 639
        y_scale = ((1 << (frac + 1)) + 239) // 479
        x_off   = 5 << (frac - 1)
        y_off   = 1 << frac

        c_x = x_pos * x_scale - x_off
        c_y = y_pos * y_scale - y_off

        if ((x_t < 640) and (y_t < 480)):
            count = find_count(c_x, c_y, frac)
        else:
            count = 0

        red = colors[count][0]
        green = colors[count][1]
        blue = colors[count][2]

        hsync = int(not ((656 <= x_t) and (751 >= x_t)))
        vsync = int(not ((490 <= y_t) and (491 >= y_t)))
        video_active = int((639 >= x_t) and (479 >= y_t))

        uo_out = 0
        if (video_active):
            if (red // 2 == 1):
                uo_out += 1
            if (green // 2 == 1):
                uo_out += 2
            if (blue // 2 == 1):
                uo_out += 4
            if (red % 2 == 1):
                uo_out += 16
            if (green % 2 == 1):
                uo_out += 32
            if (blue % 2 == 1):
                uo_out += 64
        if (hsync):
            uo_out += 128
        if (vsync):
            uo_out += 8

        assert dut.uo_out.value == uo_out, f"Expected uo_out={bin(uo_out)}, got uo_out={dut.uo_out.value}"

        await FallingEdge(dut.clk)















