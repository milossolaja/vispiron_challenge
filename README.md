
## Approach

To generate tests:

    1. I initially thought of my approach and classes I am going to use.
    2. I identified critical test scenarios for each component of the system.
    3. I used Claude as a starting point to generate a comprehensive set of test cases. 
    4. After reviewing the generated tests, I selected the most relevant and valuable ones, then adapted and refined them to suit my specific implementation needs. 


Prompt that I used:
```
I am developing a color brightness calculator and name finder, write test cases using python unittest that cover:
1. Color Parsing Tests:
   * Parse standard hex colors with and without # prefix
   * Verify correct RGB component extraction
2. Brightness Calculation Tests:
   * Calculate brightness for white (maximum brightness)
   * Calculate brightness for black (minimum brightness)
   * Calculate brightness for primary colors (red, green, blue)
   * Verify precision of formula: sqrt(0.241*R^2 + 0.691*G^2 + 0.068*B^2)
3. API Integration Tests:
   * Mock successful API responses with sample color data
   * Handle API failure (404 responses)
   * Handle network exceptions
   * Verify proper extraction of color names
4. Color Matching Tests:
   * Find exact matches by hex code
   * Find closest matches for similar colors
5. Integration Tests:
   * End-to-end test with sample inputs
   * Verify brightest color selection from a list
   * Confirm correct RGB values and name assignment
   * Test string representation format
   
Include edge cases like empty color lists and API errors to ensure robustness.

I will have 2 classes in main:
1. Class to represent a color with RGB components and brightness calculation called "Color"
2. Class to find the brightest color from a list of hex color codes called "BrightestColorFinder"

This is API response that is returned with all available colors:

{
	"status": 200,
	"statusText": "OK",
	"message": "All css colors retrieved.",
	"count": 148,
	"colors": [
		{
			"name": "AliceBlue",
			"theme": "light",
			"group": "Gray",
			"hex": "F0F8FF",
			"rgb": "240,248,255"
		},
		{
			"name": "AntiqueWhite",
			"theme": "light",
			"group": "Gray",
			"hex": "FAEBD7",
			"rgb": "250,235,215"
		},
...
]
}

I will calculate closest matching color using Euclidean distance

```

### Structure

```
vispiron_task/
│
├── __init__.py           # Makes the folder a package
├── main.py               # Entry point for the application
├── tests.py              # Unittest tests 
│
├── models/               # Core data models
│   ├── __init__.py
│   └── color.py          # Contains the Color class
│
├── services/             # Services for additional functionality
│   ├── __init__.py
│   └── color_api.py      # API interaction logic
│
└── utils/                # Utility functions and helper classes
    ├── __init__.py
    └── color_finder.py   # Contains the BrightestColorFinder class
```

### Run

To run script including example
```
python main.py
```

To run tests:
```
python tests.py 
python -m unittest
```

## Exercise text

Hexadecimal color values are used for color values in frontend programming

 I.e. the RGB components are coded as hexadecimal values in the interval from 00 to FF, where FF corresponds to the decimal number 255

(F = 15, FF = 15 * 16 + 15 * 1 = 240 + 15 = 255)

In this representation, the color 'white' is coded as "#FFFFFF", the color 'black' is coded as "#000000", and 'red' is coded as "#FF0000."


The brightness of a color is determined by the formula sqrt(0.241 R^2 + 0.691 G^2 + 0.068 B^2).


Your task is to select the brightest color from a list of color values and output the red, green and blue components individually.

Demonstrate that you can use principles of object-oriented design in a meaningful way, as well as master the standard Python APIs.


Example input: list = ["#AABBCC", "#154331", "#A0B1C2", "#000000", "#FFFFFF"]

Output to the example input: "The brightest color is: #FFFFFF (r=255, g=255, b=255)"


Please also make sure to tell/show me how you tested the correctness of your functionality.

### Bonus

As a bonus (if you have some time left and/or some extra motivation):

Enhance the output by the name of the brightest color.

To solve this task, please use the API posted at https://www.csscolorsapi.com/ in your Python source code and implement an algorithm to find the most suitable color name.


For the example input list from above the expected output would be: „The brightest color is: #FFFFFF (r=255, g=255, b=255), called White“