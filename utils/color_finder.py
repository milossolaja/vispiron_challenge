from typing import List, Optional
from models.color import Color
from services.color_api import ColorApiService


class BrightestColorFinder:
    """
    Class to find the brightest color from a list of hex color codes.
    """
    def __init__(self, color_list: List[str]) -> None:
        """
        Initialize with a list of hex color codes.
        
        Args:
            color_list: A list of hex color strings.
        """
        self.colors: List[Color] = [Color(color) for color in color_list]

    def find_brightest(self) -> Optional[Color]:
        """
        Find the color with the highest brightness value.
        
        Returns:
            The Color object with the highest brightness, or None if the list is empty.
        """
        if not self.colors:
            return None

        return max(self.colors, key=lambda color: color.brightness)

    def find_brightest_with_name(self) -> Optional[Color]:
        """
        Find the brightest color and fetch its name.
        
        Returns:
            The brightest Color object with its name set, or None if the list is empty.
        """
        brightest = self.find_brightest()
        if brightest:
            ColorApiService.find_closest_color_name(brightest)
        return brightest