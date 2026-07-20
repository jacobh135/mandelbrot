import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def reset_dut(dut):
    dut.rst_n.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

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
async def test_cranker(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    frac = 15

    for i in range(640 * 480):
        
        x_pos = i % 640
        y_pos = i // 640

        c_x = x_pos * round(3.5 / 639 * (2 ** frac)) - round(2.5 * (2 ** frac))
        c_y = y_pos * round(2 / 479 * (2 ** frac)) - 1 * (2 ** frac)

        count = find_count(c_x, c_y, frac)

        dut.c_x.value = c_x
        dut.c_y.value = c_y
        dut.enable.value = 1

        await FallingEdge(dut.clk)

        dut.enable.value = 0

        while (dut.cranker_done.value == 0):
            await FallingEdge(dut.clk)

        assert dut.count.value == count, f"Expected count={count}, got count={dut.count.value}"