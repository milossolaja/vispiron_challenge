from typing import List, Dict, Any, Optional
import math
import requests
from models.color import Color


class ColorApiService:
    """
    Service class for interacting with the color API
    """
    API_URL: str = "https://www.csscolorsapi.com/api/colors"

    @staticmethod
    def fetch_color_names() -> Optional[List[Dict[str, Any]]]:
        """
        Fetch color names from CSS Colors API
        """
        try:
            response = requests.get(ColorApiService.API_URL)

            if response.status_code == 200:
                data = response.json()
                return data['colors']
            else:
                return None
        except Exception:
            return None

    @staticmethod
    def find_closest_color_name(color: Color) -> None:
        """
        Find the closest color name for a given Color object
        """
        colors = ColorApiService.fetch_color_names()

        if colors is None:
            color.set_name('Unknown')
            return

        min_distance: float = float('inf')
        closest_color: Optional[str] = None

        hex_code_normalized = color.hex_code.lstrip('#')

        for color_data in colors:
            if color_data['hex'].upper() == hex_code_normalized:
                color.set_name(color_data['name'])
                return

            try:
                r = int(color_data['hex'][0:2], 16)
                g = int(color_data['hex'][2:4], 16)
                b = int(color_data['hex'][4:6], 16)
                # Euclidean distance in RGB space
                distance = math.sqrt((color.r - r)**2 +
                                     (color.g - g)**2 + (color.b - b)**2)

                if distance < min_distance:
                    min_distance = distance
                    closest_color = color_data['name']
            except (ValueError, IndexError):
                # Skip invalid color hex values
                continue

        color.set_name(closest_color)
