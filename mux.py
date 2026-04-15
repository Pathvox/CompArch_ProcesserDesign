def mux2(input0: int, input1: int, select: int) -> int:
    if select not in (0, 1):
        raise ValueError(f"MUX2 select must be 0 or 1, got {select}")
    return input1 if select else input0


def muxN(inputs: list[int], select: int) -> int:
    if not (0 <= select < len(inputs)):
        raise IndexError(
            f"MUX select {select} out of range for {len(inputs)}-input MUX"
        )
    return inputs[select]