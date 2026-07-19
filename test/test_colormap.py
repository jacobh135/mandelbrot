import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.test()
async def test_colormap(dut):
    
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

    for i in range(32):
        dut.count.value = i

        await Timer(1, unit="ns")

        assert dut.red.value == colors[i][0], f"Expected red={colors[i][0]}, got red={dut.red.value}"
        assert dut.green.value == colors[i][1], f"Expected green={colors[i][1]}, got green={dut.green.value}"
        assert dut.blue.value == colors[i][2], f"Expected blue={colors[i][2]}, got blue={dut.blue.value}"