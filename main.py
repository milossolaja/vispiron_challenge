from typing import List
from utils.color_finder import BrightestColorFinder


def main() -> None:
    """
    Main function to demonstrate the color analyzer functionality.
    """
    # Example input
    color_list: List[str] = ["#AABBCC", "#154331", "#A0B1C2", "#000000", "#FFFFFF"]
    finder = BrightestColorFinder(color_list)
    brightest = finder.find_brightest_with_name()

    if brightest:
        print(f"The brightest color is: {brightest}")
    else:
        print("No colors provided")


if __name__ == "__main__":
    main()