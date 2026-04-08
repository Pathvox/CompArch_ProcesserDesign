"""
main.py  —  Entry point for the Memory Hierarchy Simulation
CSC 4210/6210 Computer Architecture - Task 3
"""

import sys

from memoryhierarchy import MemoryHierarchy, ReplacementPolicy


def demo_basic():
    """Basic end-to-end run: load 10 instructions, simulate 80 cycles."""
    print("\n" + "="*55)
    print("  DEMO 1 — Basic Simulation (LRU Cache)")
    print("="*55)

    sim = MemoryHierarchy(
        ssd_size=1024, dram_size=256, l3_size=64, l2_size=16, l1_size=4,
        ssd_latency=20, dram_latency=10, l3_latency=5, l2_latency=3, l1_latency=1,
        ssd_bw=4, dram_bw=8,
        policy=ReplacementPolicy.LRU,
    )
    sim.print_config()

    # Build a small program
    program = [0xADD10001 + i for i in range(10)]
    sim.load_program(program)

    # Demonstrate a read hit/miss before the clock runs
    sim.read(program[0])   # will be a miss (nothing in cache yet)

    sim.run(cycles=80)
    sim.print_log()
    sim.print_summary()


def demo_fifo():
    """Smaller memory sizes to trigger eviction, using FIFO policy."""
    print("\n" + "="*55)
    print("  DEMO 2 — Eviction Demo (FIFO Cache, tight sizes)")
    print("="*55)

    sim = MemoryHierarchy(
        ssd_size=32, dram_size=16, l3_size=8, l2_size=4, l1_size=2,
        ssd_latency=5, dram_latency=3, l3_latency=2, l2_latency=1, l1_latency=1,
        ssd_bw=2, dram_bw=4,
        policy=ReplacementPolicy.FIFO,
    )
    sim.print_config()

    program = [0xBEEF0000 + i for i in range(20)]
    sim.load_program(program)
    sim.run(cycles=60)
    sim.print_log()
    sim.print_summary()


def demo_write_back():
    """Show write-back propagation down the hierarchy."""
    print("\n" + "="*55)
    print("  DEMO 3 — Write-Back Operation")
    print("="*55)

    sim = MemoryHierarchy(
        ssd_size=64, dram_size=32, l3_size=16, l2_size=8, l1_size=4,
        ssd_latency=10, dram_latency=5, l3_latency=3, l2_latency=2, l1_latency=1,
        policy=ReplacementPolicy.RANDOM,
    )
    sim.print_config()

    program = [0xCAFE0000 + i for i in range(5)]
    sim.load_program(program)
    sim.run(cycles=40)

    # After execution, write back one instruction
    sim.write_back(0xCAFE0000)

    sim.print_log()
    sim.print_summary()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    demo_basic()
    demo_fifo()
    demo_write_back()
