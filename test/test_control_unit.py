import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_control_unit(dut):

    x_t = -1
    y_t = 0

    dut.x_t.value = x_t
    dut.y_t.value = y_t
    dut.cranker_done.value = 0

    await Timer (1, unit="ns")

    cranker_enable = 1
    count_advance = 1

    assert dut.time_enable.value == 0, f"Expected time_enable={0}, got time_enable={dut.time_enable.value}"
    assert dut.count_capture.value == 0, f"Expected count_capture={0}, got count_capture={dut.count_capture.value}"

    assert dut.cranker_enable.value == cranker_enable, f"Expected cranker_enable={cranker_enable}, got cranker_enable={dut.cranker_enable.value}"
    assert dut.count_advance.value == count_advance, f"Expected count_advance={count_advance}, got count_advance={dut.count_advance.value}"


    for i in range(800 * 525):
        x_t = i % 800
        y_t = i // 800

        dut.x_t.value = x_t
        dut.y_t.value = y_t

        await Timer (1, unit="ns")

        cranker_enable = int((x_t % 32 == 0 or x_t == -1) and (x_t < 640) and (y_t < 480))
        count_advance = int((x_t % 32 == 31) and (x_t < 640) and (y_t < 480))

        assert dut.time_enable.value == 0, f"Expected time_enable={0}, got time_enable={dut.time_enable.value}"
        assert dut.count_capture.value == 0, f"Expected count_capture={0}, got count_capture={dut.count_capture.value}"

        assert dut.cranker_enable.value == cranker_enable, f"Expected cranker_enable={cranker_enable}, got cranker_enable={dut.cranker_enable.value}"
        assert dut.count_advance.value == count_advance, f"Expected count_advance={count_advance}, got count_advance={dut.count_advance.value}"

    dut.cranker_done.value = 1

    await Timer (1, unit="ns")

    assert dut.time_enable.value == 1, f"Expected time_enable={1}, got time_enable={dut.time_enable.value}"
    assert dut.count_capture.value == 1, f"Expected count_capture={1}, got count_capture={dut.count_capture.value}"
        

        
