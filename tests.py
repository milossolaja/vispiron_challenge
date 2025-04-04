import unittest
import math
from unittest.mock import patch, Mock
from utils.color_finder import BrightestColorFinder
from models.color import Color
from services.color_api import ColorApiService


class TestColor(unittest.TestCase):
    def test_parse_hex_code(self):
        color = Color("#FFFFFF")
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 255)
        self.assertEqual(color.b, 255)

        color = Color("#000000")
        self.assertEqual(color.r, 0)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 0)

        color = Color("#FF0000")
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 0)

        # Test without #
        color = Color("00FF00")
        self.assertEqual(color.r, 0)
        self.assertEqual(color.g, 255)
        self.assertEqual(color.b, 0)

    def test_calculate_brightness(self):
        white = Color("#FFFFFF")
        self.assertAlmostEqual(white.brightness, 255, places=2)

        black = Color("#000000")
        self.assertAlmostEqual(black.brightness, 0, places=2)

        red = Color("#FF0000")
        expected_brightness = round(math.sqrt(0.241 * 255**2), 2)
        self.assertAlmostEqual(red.brightness, expected_brightness, places=2)

        green = Color("#00FF00")
        expected_brightness = round(math.sqrt(0.691 * 255**2), 2)
        self.assertAlmostEqual(green.brightness, expected_brightness, places=2)

        blue = Color("#0000FF")
        expected_brightness = round(math.sqrt(0.068 * 255**2), 2)
        self.assertAlmostEqual(blue.brightness, expected_brightness, places=2)


class TestColorApiService(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_color_names(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "statusText": "OK",
            "message": "All css colors retrieved.",
            "count": 3,
            "colors": [
                {"name": "White", "hex": "FFFFFF", "rgb": "255,255,255"},
                {"name": "Black", "hex": "000000", "rgb": "0,0,0"},
                {"name": "Red", "hex": "FF0000", "rgb": "255,0,0"}
            ]
        }
        mock_get.return_value = mock_response

        color_data = ColorApiService.fetch_color_names()
        self.assertEqual(len(color_data), 3)
        self.assertEqual(color_data[0]["name"], "White")

        mock_response.status_code = 404
        self.assertIsNone(ColorApiService.fetch_color_names())

        mock_get.side_effect = Exception("API Connection Error")
        self.assertIsNone(ColorApiService.fetch_color_names())

    @patch('requests.get')
    def test_find_closest_color_name(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "statusText": "OK",
            "message": "All css colors retrieved.",
            "count": 3,
            "colors": [
                {"name": "White", "hex": "FFFFFF", "rgb": "255,255,255"},
                {"name": "Black", "hex": "000000", "rgb": "0,0,0"},
                {"name": "Red", "hex": "FF0000", "rgb": "255,0,0"}
            ]
        }
        mock_get.return_value = mock_response

        # Almost black
        color = Color("#001000")
        ColorApiService.find_closest_color_name(color)
        self.assertEqual(color.name, "Black")

        # Almost white
        color = Color("#FFFFFE")
        ColorApiService.find_closest_color_name(color)
        self.assertEqual(color.name, "White")

        # Test with API failure
        mock_response.status_code = 404
        color = Color("#FFFFFF")
        ColorApiService.find_closest_color_name(color)

        self.assertEqual(color.name, "Unknown")

    @patch('requests.get')
    def test_find_closest_color_name_with_api_error(self, mock_get):
        mock_get.side_effect = Exception("API Connection Error")

        color = Color("#FFFFFF")
        ColorApiService.find_closest_color_name(color)
        self.assertEqual(color.name, "Unknown")


class TestBrightestColorFinder(unittest.TestCase):
    def test_find_brightest(self):
        colors = ["#AABBCC", "#154331", "#A0B1C2", "#000000", "#FFFFFF"]
        finder = BrightestColorFinder(colors)
        brightest = finder.find_brightest()

        self.assertEqual(brightest.hex_code, "#FFFFFF")

    def test_empty_list(self):
        finder = BrightestColorFinder([])
        self.assertIsNone(finder.find_brightest())

    @patch('services.color_api.ColorApiService.fetch_color_names')
    def test_find_brightest_with_name(self, mock_fetch_color_names):
        # Mock the color data
        mock_fetch_color_names.return_value = [
            {"name": "White", "hex": "FFFFFF", "rgb": "255,255,255"},
            {"name": "Black", "hex": "000000", "rgb": "0,0,0"},
            {"name": "Red", "hex": "FF0000", "rgb": "255,0,0"}
        ]

        colors = ["#AABBCC", "#154331", "#A0B1C2", "#000000", "#FFFFFF"]
        finder = BrightestColorFinder(colors)
        brightest = finder.find_brightest_with_name()

        self.assertEqual(brightest.hex_code, "#FFFFFF")
        self.assertEqual(brightest.name, "White")


class TestIntegration(unittest.TestCase):
    @patch('services.color_api.ColorApiService.fetch_color_names')
    def test_example_input(self, mock_fetch_color_names):
        # Mock the color data
        mock_fetch_color_names.return_value = [
            {"name": "White", "hex": "FFFFFF", "rgb": "255,255,255"},
            {"name": "Black", "hex": "000000", "rgb": "0,0,0"},
            {"name": "Red", "hex": "FF0000", "rgb": "255,0,0"},
            {"name": "Green", "hex": "00FF00", "rgb": "0,255,0"},
            {"name": "Blue", "hex": "0000FF", "rgb": "0,0,255"}
        ]

        # Test with the example input from the problem statement
        color_list = ["#AABBCC", "#154331", "#A0B1C2", "#000000", "#FFFFFF"]
        finder = BrightestColorFinder(color_list)
        brightest = finder.find_brightest_with_name()

        self.assertEqual(brightest.hex_code, "#FFFFFF")
        self.assertEqual(brightest.r, 255)
        self.assertEqual(brightest.g, 255)
        self.assertEqual(brightest.b, 255)
        self.assertEqual(brightest.name, "White")

        # Check the string representation
        self.assertEqual(
            str(brightest),
            "#FFFFFF (r=255, g=255, b=255), called White")


if __name__ == '__main__':
    unittest.main()
