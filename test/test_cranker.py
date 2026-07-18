import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles

def adjust(num, frac):
    num %= (2 ** (frac + 3))
    if (num >= (2 ** (frac + 2))):
        num -= (2 ** (frac + 3))

    return num

def find_out(c_x, c_y, frac):
    z_x = 0
    z_y = 0
    count = 0
    while ((z_x ** 2 + z_y ** 2 < 4 * (2 ** frac) ** 2) and (count < 24)):
        z_x_new = adjust((z_x ** 2) // (2 ** frac) - (z_y ** 2) // (2 ** frac) + c_x, frac)
        z_y_new = adjust(2 * ((z_x * z_y) // (2 ** frac)) + c_y, frac)
        z_x = z_x_new
        z_y = z_y_new
        count += 1
    return count

@cocotb.test()
async def test_cranker(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    frac = 15

    # load initial state
    dut.rst_n.value = 0
    dut.c_x.value = 0
    dut.c_y.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

    # compute expected out
    out = find_out(0, 0, frac)

    # prepare next c inputs
    dut.c_x.value = 1 * round(3.5 / 639 * (2 ** frac)) - round(2.5 * (2 ** frac))
    dut.c_y.value = 0 * round(2 / 479 * (2 ** frac)) - 1 * (2 ** frac)

    # receive inputs & advance
    await FallingEdge(dut.clk)
    count = 0

    # run DUT
    while (dut.cranker_done.value == 0):
        await FallingEdge(dut.clk)
        count += 1
    
    # check out
    assert out == dut.out.value, f"Expected out={out}, got out={dut.out.value}"
    assert count == 24, f"Expected count=24, got count={count}"

    for i in range (1, 640 * 480):

        # compute expected out
        x_pos = i % 640
        y_pos = i // 640

        c_x = x_pos * round(3.5 / 639 * (2 ** frac)) - round(2.5 * (2 ** frac))
        c_y = y_pos * round(2 / 479 * (2 ** frac)) - 1 * (2 ** frac)

        out = find_out(c_x, c_y, frac)

        # prepare next c inputs
        x_pos = (i + 1) % 640
        y_pos = (i + 1) // 640

        dut.c_x.value = x_pos * round(3.5 / 639 * (2 ** frac)) - round(2.5 * (2 ** frac))
        dut.c_y.value = y_pos * round(2 / 479 * (2 ** frac)) - 1 * (2 ** frac)

        # receive inputs & advance
        await FallingEdge(dut.clk)
        count = 0

        # run DUT
        while (dut.cranker_done.value == 0):
            await FallingEdge(dut.clk)
            count += 1
        
        # check out
        assert out == dut.out.value, f"Expected out={out}, got out={dut.out.value}"
        assert count == 24, f"Expected count=24, got count={count}"