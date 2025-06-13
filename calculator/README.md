# Calculator Application

A simple command-line calculator application that evaluates mathematical expressions following operator precedence rules.

## Features

- Supports basic arithmetic operations: addition (+), subtraction (-), multiplication (*), and division (/)
- Follows standard operator precedence rules (multiplication/division before addition/subtraction)
- Presents results in a visually appealing box format
- Handles errors gracefully

## Installation

No additional installation is required beyond having Python 3.x installed.

## Usage

Run the calculator from the command line by providing a mathematical expression as an argument:

```bash
python main.py "<expression>"
```

For example:

```bash
python main.py "3 + 5"
python main.py "10 - 2 * 3"
python main.py "(8 + 2) * 5"
```

## Project Structure

- `main.py` - Entry point for the application
- `pkg/calculator.py` - Contains the Calculator class that evaluates expressions
- `pkg/render.py` - Formats the output in a nice visual box
- `tests.py` - Unit tests for the calculator functionality

## Testing

Run the tests to verify that the calculator is working correctly:

```bash
python tests.py
```

## Examples

**Input:**
```
python main.py "3 + 5"
```

**Output:**
```
┌──────────┐
│  3 + 5   │
│          │
│  =       │
│          │
│  8       │
└──────────┘
```

**Input:**
```
python main.py "3 + 7 * 2"
```

**Output:**
```
┌──────────────┐
│  3 + 7 * 2   │
│              │
│  =           │
│              │
│  17          │
└──────────────┘
```

## License

MIT