import cocotb
from cocotb.triggers import Timer, ReadOnly

@cocotb.test()
async def test_pattern_generator(dut):       
    for i in range(800):
        dut.x_pos.value = i
        if (i > 639):
            dut.video_active.value = 0
        else:
            dut.video_active.value = 1
        
        await Timer(1, unit="ns")
        if (i <= 639):
            red = (i // 128) % 2
            green = (i // 64) % 2
            blue = (i // 32) % 2
            red *= 3
            green *= 3
            blue *= 3
        else:
            red = 0
            green = 0
            blue = 0
        assert red == dut.red.value, f"Expected red={red}, got red={dut.red.value}"
        assert green == dut.green.value, f"Expected green={green}, got green={dut.green.value}"
        assert blue == dut.blue.value, f"Expected blue={blue}, got blue={dut.blue.value}"
        