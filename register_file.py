class RegisterFile:
    NUM_REGISTERS = 8  # t0 – t7

    def __init__(self):
        """Initialize all registers to 0."""
        self._regs: list[int] = [0] * self.NUM_REGISTERS

    def read(self, reg_num: int) -> int:
        self._validate(reg_num)
        return self._regs[reg_num] & 0xFFFF_FFFF

    def write(self, reg_num: int, value: int, write_enable: bool = True) -> None:
        if not write_enable:
            return
        self._validate(reg_num)
        self._regs[reg_num] = value & 0xFFFF_FFFF

    def load(self, values: dict[int, int]) -> None:
        for reg, val in values.items():
            self.write(reg, val)

    def dump(self) -> dict[str, int]:
        return {f"t{i}": self._regs[i] for i in range(self.NUM_REGISTERS)}

    def _validate(self, reg_num: int) -> None:
        if not (0 <= reg_num < self.NUM_REGISTERS):
            raise ValueError(
                f"Register index {reg_num} out of range "
                f"(0–{self.NUM_REGISTERS - 1})"
            )