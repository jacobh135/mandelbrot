import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_pixel_generator(dut):
    
    x_t = -1
    y_t = 0

    dut.x_t.value = x_t
    dut.y_t.value = y_t

    await Timer(1, unit="ns")

    x_pos = 0
    y_pos = 0
    assert dut.x_pos.value == x_pos, f"Expected x_pos={x_pos}, got x_pos={dut.x_pos.value}"
    assert dut.y_pos.value == y_pos, f"Expected y_pos={y_pos}, got y_pos={dut.y_pos.value}"

    for i in range(800 * 525):
        x_t = i % 640
        y_t = i // 640

        dut.x_t.value = x_t
        dut.y_t.value = y_t

        await Timer(1, unit="ns")

        x_sum = x_t + 32
        y_sum = y_t

        if ((x_sum >= 640) | (y_sum >= 480)):
            x_sum = 0
            if (y_sum >= 479):
                y_sum = 0
            else:
                y_sum += 1

        x_pos = (x_sum // 32) * 32
        y_pos = (y_sum // 32) * 32

        assert dut.x_pos.value == x_pos, f"Expected x_pos={x_pos}, got x_pos={dut.x_pos.value}"
        assert dut.y_pos.value == y_pos, f"Expected y_pos={y_pos}, got y_pos={dut.y_pos.value}"