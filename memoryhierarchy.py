"""
Memory Hierarchy Simulation (SSD → DRAM → Cache)
CSC 4210/6210 Computer Architecture - Task 3
Georgia State University, Spring 2026
"""

import random
from collections import OrderedDict
from enum import Enum


# ─────────────────────────────────────────────
#  Enums & Constants
# ─────────────────────────────────────────────

class ReplacementPolicy(Enum):
    LRU    = "LRU"
    FIFO   = "FIFO"
    RANDOM = "Random"


# ─────────────────────────────────────────────
#  Memory Level Base Class
# ─────────────────────────────────────────────

class MemoryLevel:
    """Abstract base for any memory level in the hierarchy."""

    def __init__(self, name: str, capacity: int, latency: int, bandwidth: int):
        """
        Parameters
        ----------
        name      : human-readable label (e.g. "SSD", "L1")
        capacity  : max number of 32-bit instructions storable
        latency   : clock cycles needed to complete one transfer
        bandwidth : max instructions moved per cycle (0 = unlimited)
        """
        self.name      = name
        self.capacity  = capacity
        self.latency   = latency
        self.bandwidth = bandwidth
        self.storage: list[int] = []   # list of 32-bit instruction words

    # ── helpers ──────────────────────────────

    def is_full(self) -> bool:
        return len(self.storage) >= self.capacity

    def free_slots(self) -> int:
        return self.capacity - len(self.storage)

    def has_data(self) -> bool:
        return len(self.storage) > 0

    def peek(self) -> int | None:
        return self.storage[0] if self.storage else None

    def pop_front(self) -> int | None:
        return self.storage.pop(0) if self.storage else None

    def push(self, instruction: int) -> bool:
        if self.is_full():
            return False
        self.storage.append(instruction)
        return True

    def __repr__(self):
        return (f"[{self.name}] capacity={self.capacity} | "
                f"used={len(self.storage)} | latency={self.latency}cy | "
                f"bw={self.bandwidth or '∞'}/cy")


# ─────────────────────────────────────────────
#  Cache Layer  (LRU / FIFO / Random eviction)
# ─────────────────────────────────────────────

class CacheLevel(MemoryLevel):
    """Cache level with optional replacement policy."""

    def __init__(self, name: str, capacity: int, latency: int,
                 bandwidth: int, policy: ReplacementPolicy = ReplacementPolicy.LRU):
        super().__init__(name, capacity, latency, bandwidth)
        self.policy  = policy
        self.hits    = 0
        self.misses  = 0
        # For LRU we use an OrderedDict  {instruction: None}
        self._lru_order: OrderedDict[int, None] = OrderedDict()
        # For FIFO we reuse self.storage (list); for Random too.

    # ── lookup ───────────────────────────────

    def lookup(self, instruction: int) -> bool:
        """Check for a cache hit; update LRU order if relevant."""
        found = instruction in self.storage
        if found:
            self.hits += 1
            if self.policy == ReplacementPolicy.LRU:
                self.storage.remove(instruction)
                self.storage.append(instruction)   # move to MRU end
        else:
            self.misses += 1
        return found

    # ── eviction ─────────────────────────────

    def evict(self) -> int | None:
        """Remove and return one instruction according to the policy."""
        if not self.storage:
            return None
        if self.policy == ReplacementPolicy.LRU:
            victim = self.storage[0]        # LRU end
            self.storage.pop(0)
        elif self.policy == ReplacementPolicy.FIFO:
            victim = self.storage[0]
            self.storage.pop(0)
        else:  # RANDOM
            idx    = random.randrange(len(self.storage))
            victim = self.storage[idx]
            self.storage.pop(idx)
        return victim

    def load(self, instruction: int) -> int | None:
        """
        Insert instruction into cache.
        Returns evicted instruction if the cache was full, else None.
        """
        evicted = None
        if self.is_full():
            evicted = self.evict()
        self.storage.append(instruction)
        return evicted

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


# ─────────────────────────────────────────────
#  Transfer Manager  (clock-driven)
# ─────────────────────────────────────────────

class PendingTransfer:
    """One in-flight data-movement task between two levels."""

    def __init__(self, src: MemoryLevel, dst: MemoryLevel,
                 instructions: list[int], cycles_remaining: int):
        self.src               = src
        self.dst               = dst
        self.instructions      = instructions      # payload
        self.cycles_remaining  = cycles_remaining

    def tick(self) -> bool:
        """Advance one cycle. Returns True when the transfer completes."""
        self.cycles_remaining -= 1
        return self.cycles_remaining <= 0

    def commit(self, log: list[str], clock: int):
        """Push payload into destination; log the event."""
        for instr in self.instructions:
            placed = self.dst.push(instr)
            if not placed:
                log.append(f"  [CLK {clock}] ⚠  {self.dst.name} full — "
                            f"instruction 0x{instr:08X} dropped!")
            else:
                log.append(f"  [CLK {clock}] ✓  0x{instr:08X}  "
                            f"{self.src.name} → {self.dst.name}")


# ─────────────────────────────────────────────
#  Memory Hierarchy Simulation
# ─────────────────────────────────────────────

class MemoryHierarchy:
    """
    Coordinates the full SSD → DRAM → L3 → L2 → L1 → CPU pipeline.

    Parameters
    ----------
    ssd_size, dram_size : int  (# instructions)
    l3_size, l2_size, l1_size : int
    ssd_latency … l1_latency  : int  (clock cycles per transfer)
    ssd_bw … l1_bw            : int  (instructions/cycle; 0 = unlimited)
    policy                    : ReplacementPolicy for all cache levels
    """

    def __init__(
        self,
        ssd_size:   int = 1024,
        dram_size:  int = 256,
        l3_size:    int = 64,
        l2_size:    int = 16,
        l1_size:    int = 4,
        ssd_latency:  int = 20,
        dram_latency: int = 10,
        l3_latency:   int = 5,
        l2_latency:   int = 3,
        l1_latency:   int = 1,
        ssd_bw:   int = 4,
        dram_bw:  int = 8,
        l3_bw:    int = 0,
        l2_bw:    int = 0,
        l1_bw:    int = 0,
        policy: ReplacementPolicy = ReplacementPolicy.LRU,
    ):
        # ── validate hierarchy sizes ──────────
        assert ssd_size > dram_size > l3_size > l2_size > l1_size, (
            "Hierarchy violation: SSD > DRAM > L3 > L2 > L1 required")

        # ── build levels ──────────────────────
        self.ssd  = MemoryLevel("SSD",  ssd_size,  ssd_latency,  ssd_bw)
        self.dram = MemoryLevel("DRAM", dram_size, dram_latency, dram_bw)
        self.l3   = CacheLevel ("L3",   l3_size,   l3_latency,   l3_bw,  policy)
        self.l2   = CacheLevel ("L2",   l2_size,   l2_latency,   l2_bw,  policy)
        self.l1   = CacheLevel ("L1",   l1_size,   l1_latency,   l1_bw,  policy)

        # Ordered pipeline for iteration
        self.levels: list[MemoryLevel] = [
            self.ssd, self.dram, self.l3, self.l2, self.l1
        ]

        self.cpu_executed:  list[int]  = []   # instructions fetched by CPU
        self.clock:         int        = 0
        self.log:           list[str]  = []
        self._transfers:    list[PendingTransfer] = []

    # ── public helpers ───────────────────────

    def load_program(self, instructions: list[int]):
        """Pre-load instructions into SSD."""
        for instr in instructions:
            if not self.ssd.push(instr):
                self.log.append("⚠  SSD full — cannot load more instructions.")
                break
        self.log.append(
            f"Program loaded: {len(self.ssd.storage)} instruction(s) in SSD.")

    def _bandwidth_cap(self, level: MemoryLevel, available: int) -> int:
        """Return how many instructions may transfer this cycle."""
        if level.bandwidth == 0:
            return available
        return min(level.bandwidth, available)

    def _schedule_transfer(self, src: MemoryLevel, dst: MemoryLevel):
        """
        Pop up to bandwidth-limit instructions from src and schedule
        a PendingTransfer to dst that completes after src.latency cycles.
        """
        n        = self._bandwidth_cap(src, min(src.free_slots() if hasattr(dst,'storage') else src.capacity, len(src.storage)))
        n        = self._bandwidth_cap(src, len(src.storage))
        n        = min(n, dst.free_slots())
        if n == 0:
            return
        payload  = [src.pop_front() for _ in range(n)]
        transfer = PendingTransfer(src, dst, payload, src.latency)
        self._transfers.append(transfer)
        self.log.append(
            f"  [CLK {self.clock}] ↑  Scheduled {n} instr(s) "
            f"{src.name}→{dst.name} (completes in {src.latency} cycle(s))")

    # ── clock tick ───────────────────────────

    def tick(self):
        """Advance simulation by one clock cycle."""
        self.clock += 1
        self.log.append(f"\n── Clock Cycle {self.clock} ──────────────────")

        # 1. Advance in-flight transfers
        completed = []
        for t in self._transfers:
            if t.tick():
                completed.append(t)
        for t in completed:
            self._transfers.remove(t)
            t.commit(self.log, self.clock)

        # 2. Schedule new transfers up the hierarchy if capacity allows
        pairs = [
            (self.ssd,  self.dram),
            (self.dram, self.l3),
            (self.l3,   self.l2),
            (self.l2,   self.l1),
        ]
        for src, dst in pairs:
            if src.has_data() and not dst.is_full():
                self._schedule_transfer(src, dst)

        # 3. CPU fetches from L1
        if self.l1.has_data():
            instr = self.l1.pop_front()
            self.cpu_executed.append(instr)
            self.log.append(
                f"  [CLK {self.clock}] ⚡ CPU executed  0x{instr:08X}")

        # 4. Log current state
        self._log_state()

    def _log_state(self):
        parts = []
        for lvl in self.levels:
            parts.append(f"{lvl.name}:{len(lvl.storage)}/{lvl.capacity}")
        self.log.append("  State → " + "  |  ".join(parts))

    # ── read / write operations ───────────────

    def read(self, instruction: int) -> str:
        """
        Attempt to read a specific instruction from cache levels
        (L1 first, then L2, then L3 — cache-hit path).
        Returns the level where the hit occurred, or 'MISS'.
        """
        for cache in [self.l1, self.l2, self.l3]:
            if cache.lookup(instruction):
                self.log.append(
                    f"  READ  0x{instruction:08X}  → HIT in {cache.name} "
                    f"(hit_rate={cache.hit_rate:.1%})")
                return cache.name
        self.log.append(
            f"  READ  0x{instruction:08X}  → MISS (will load from hierarchy)")
        return "MISS"

    def write_back(self, instruction: int):
        """
        Write-back: propagate an instruction down from L1 toward SSD
        following the strict hierarchy (no skipping).
        The instruction is appended to each lower level that has room.
        """
        self.log.append(f"  WRITE-BACK  0x{instruction:08X}")
        order = [self.l1, self.l2, self.l3, self.dram, self.ssd]
        for i, lvl in enumerate(order[:-1]):
            nxt = order[i + 1]
            nxt.push(instruction)
            self.log.append(f"    0x{instruction:08X} written to {nxt.name}")

    # ── run ──────────────────────────────────

    def run(self, cycles: int):
        """Run the simulation for a given number of clock cycles."""
        self.log.append(f"\n{'='*55}")
        self.log.append(f"  Starting simulation for {cycles} clock cycle(s)")
        self.log.append(f"{'='*55}")
        for _ in range(cycles):
            self.tick()
            if (not any(lvl.has_data() for lvl in self.levels)
                    and not self._transfers):
                self.log.append("\n  ✓ All instructions executed — stopping early.")
                break

    # ── reporting ────────────────────────────

    def print_config(self):
        lines = [
            "\n╔══════════════════════════════════════════════╗",
            "║     Memory Hierarchy Configuration           ║",
            "╠══════════════════════════════════════════════╣",
        ]
        for lvl in self.levels:
            bw_str = f"{lvl.bandwidth}/cy" if lvl.bandwidth else "unlimited"
            lines.append(
                f"║  {lvl.name:<5} capacity={lvl.capacity:<6} "
                f"latency={lvl.latency:<3}cy  bw={bw_str:<10}║")
        lines.append("╚══════════════════════════════════════════════╝")
        print("\n".join(lines))

    def print_summary(self):
        print("\n" + "="*55)
        print("  SIMULATION SUMMARY")
        print("="*55)
        print(f"  Total clock cycles  : {self.clock}")
        print(f"  Instructions executed by CPU: {len(self.cpu_executed)}")
        for instr in self.cpu_executed:
            print(f"    0x{instr:08X}")

        print("\n  Cache Statistics:")
        for cache in [self.l1, self.l2, self.l3]:
            print(f"    {cache.name}  hits={cache.hits}  "
                  f"misses={cache.misses}  "
                  f"hit_rate={cache.hit_rate:.1%}")

        print("\n  Final Memory State:")
        for lvl in self.levels:
            contents = [f"0x{x:08X}" for x in lvl.storage]
            print(f"    {lvl.name:<5} [{len(lvl.storage)}/{lvl.capacity}]  "
                  f"contents: {contents if contents else '(empty)'}")
        print("="*55)

    def print_log(self):
        print("\n".join(self.log))