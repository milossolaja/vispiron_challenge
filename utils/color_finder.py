from typing import List, Optional
from models.color import Color
from services.color_api import ColorApiService


class BrightestColorFinder:
    """
    Class to find the brightest color from a list of hex color codes
    """

    def __init__(self, color_list: List[str]) -> None:
        """
        Initialize with a list of hex color codes
        """
        self.colors: List[Color] = [Color(color) for color in color_list]

    def find_brightest(self) -> Optional[Color]:
        """
        Find the color with the highest brightness value
        """
        if not self.colors:
            return None

        return max(self.colors, key=lambda color: color.brightness)

    def find_brightest_with_name(self) -> Optional[Color]:
        """
        Find the brightest color and fetch its name
        """
        brightest = self.find_brightest()
        if brightest:
            ColorApiService.find_closest_color_name(brightest)
        return brightest
