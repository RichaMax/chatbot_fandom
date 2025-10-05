from enum import StrEnum
from typing import TypeVar

T = TypeVar("T")


class SplitMethod(StrEnum):
    FILL_LAST = "fill_last"
    EQUALIZE = "equalize"


def cut_batches(
    values: list[T], batch_size: int = 50, split: SplitMethod = SplitMethod.FILL_LAST
) -> list[list[T]]:
    return [values[i : i + batch_size] for i in range(0, len(values), batch_size)]
