
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FilterOptions:
    output: str = "png"
    blur: bool = False
    black_white: bool = False
    pixelate: bool = False
    invert: bool = False
