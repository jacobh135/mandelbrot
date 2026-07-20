import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def reset_dut(dut):
    dut.rst_n.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

@cocotb.test()
async def test_file(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    dut.count.value = 0
    dut.capture.value = 0
    dut.advance.value = 0

    await FallingEdge(dut.clk)

    assert dut.active.value == 0, f"Expected active={0}, got active={dut.active.value}"

    dut.count.value = 3
    dut.capture.value = 1
    dut.advance.value = 0

    await FallingEdge(dut.clk)

    assert dut.active.value == 0, f"Expected active={0}, got active={dut.active.value}"

    dut.count.value = 0
    dut.capture.value = 0
    dut.advance.value = 1

    await FallingEdge(dut.clk)

    assert dut.active.value == 3, f"Expected active={3}, got active={dut.active.value}"

    dut.count.value = 23
    dut.capture.value = 1
    dut.advance.value = 0

    await FallingEdge(dut.clk)

    assert dut.active.value == 3, f"Expected active={3}, got active={dut.active.value}"

    dut.count.value = 0
    dut.capture.value = 0
    dut.advance.value = 1

    await FallingEdge(dut.clk)

    assert dut.active.value == 23, f"Expected active={23}, got active={dut.active.value}"