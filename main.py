import math
import requests


class Color:
    """
    Class to represent a color with RGB components and brightness calculation
    """
    def __init__(self, hex_code):
        self.hex_code = hex_code.upper()
        self.r, self.g, self.b = self.parse_hex_code()
        self.brightness = self.calculate_brightness()
        self.name = None

    def parse_hex_code(self):
        """Parse hex code into RGB components"""
        hex_code = self.hex_code.lstrip('#')
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)

        return r, g, b

    def calculate_brightness(self):
        """Brightness calculation"""
        return math.sqrt(0.241 * self.r**2 + 0.691 * self.g**2 + 0.068 * self.b**2)

    def fetch_color_names(self):
        """Fetch color names from CSS Colors API"""
        try:
            response = requests.get("https://www.csscolorsapi.com/api/colors")

            if response.status_code == 200:
                data = response.json()
                return data['colors']
            else:
                return None
        except Exception:
            return None

    def find_closest_color_name(self):
        """Find the closest color name from the provided color data"""
        colors = self.fetch_color_names()

        # Check if colors is a string (error case) and handle it
        if colors is None:
            self.name = 'Unknown'
            return

        min_distance = float('inf')
        closest_color = None

        hex_code_normalized = self.hex_code.lstrip('#')

        for color in colors:
            if color['hex'].upper() == hex_code_normalized:
                self.name = color['name']
                return

            try:
                r = int(color['hex'][0:2], 16)
                g = int(color['hex'][2:4], 16)
                b = int(color['hex'][4:6], 16)
                # Euclidean distance in RGB space
                distance = math.sqrt((self.r - r)**2 + (self.g - g)**2 + (self.b - b)**2)

                if distance < min_distance:
                    min_distance = distance
                    closest_color = color['name']
            except (ValueError, IndexError):
                # Skip invalid color hex values
                continue

        self.name = closest_color
        return

    def __str__(self):
        """String representation of the color"""
        base_str = f"{self.hex_code} (r={self.r}, g={self.g}, b={self.b})"
        return f"{base_str}, called {self.name}"


class BrightestColorFinder:
    """
    Class to find the brightest color from a list of hex color codes
    """
    def __init__(self, color_list):
        self.colors = [Color(color) for color in color_list]

    def find_brightest(self):
        """Find the color with the highest brightness value"""
        if not self.colors:
            return None

        return max(self.colors, key=lambda color: color.brightness)

    def find_brightest_with_name(self):
        """Find the brightest color and fetch its name"""
        brightest = self.find_brightest()
        if brightest:
            brightest.find_closest_color_name()
        return brightest


def main():
    # Example input
    color_list = ["#AABBCC", "#154331", "#A0B1C2", "#000000", "#FFFFFF"]
    finder = BrightestColorFinder(color_list)
    brightest = finder.find_brightest_with_name()

    if brightest:
        print(f"The brightest color is: {brightest}")
    else:
        print("No colors provided")


if __name__ == "__main__":
    main()
