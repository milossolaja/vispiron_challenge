from __future__ import annotations
import math
from typing import Optional, Tuple


class Color:
    """
    Class to represent a color with RGB components and brightness calculation
    """

    def __init__(self, hex_code: str) -> None:
        """
        Initialize a Color object with a hex code
        """
        self.hex_code: str = hex_code.upper()
        self.r: int
        self.g: int
        self.b: int
        self.r, self.g, self.b = self.parse_hex_code()
        self.brightness: float = self.calculate_brightness()
        self.name: Optional[str] = None

    def parse_hex_code(self) -> Tuple[int, int, int]:
        """
        Parse hex code into RGB components
        """
        hex_code = self.hex_code.lstrip('#')
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)

        return r, g, b

    def calculate_brightness(self) -> float:
        """
        Calculate the perceived brightness using a weighted formula
        """
        return math.sqrt(
            0.241 *
            self.r**2 +
            0.691 *
            self.g**2 +
            0.068 *
            self.b**2)

    def set_name(self, name: str) -> None:
        """
        Set the color name
        """
        self.name = name

    def __str__(self) -> str:
        """
        Get a string representation of the color
        """
        base_str = f"{self.hex_code} (r={self.r}, g={self.g}, b={self.b})"
        if self.name:
            return f"{base_str}, called {self.name}"
        return f"{base_str}"
