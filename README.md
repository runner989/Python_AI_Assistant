# AI Assistant

A command-line application that leverages Google's Gemini AI. This assistant can answer questions, generate code, fix bugs, and execute commands to solve programming problems.

## Features

- Interact with AI using natural language prompts
- Execute Python files through the AI
- Read and write files as needed to complete tasks
- Get file information and directory listings
- Maintain conversation context through multiple interactions

## Project Structure

- `main.py`: Entry point for the application
- `functions/`: Helper functions for file operations and Python execution
- `calculator/`: Example project (a calculator application) that can be interacted with

## Requirements

- Python 3.10+
- Google Gemini API key
- Required Python packages:
  - google-genai==1.12.1
  - python-dotenv==1.1.0

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the assistant with a prompt:

```bash
python main.py "your prompt here"
```

Examples:

```bash
python main.py "How do I build a calculator app?"
python main.py "fix the bug: 3 + 7 * 2 should not be 20"
python main.py "Show me the files in this project"
```

For verbose output (showing all interactions with the AI):

```bash
python main.py "your prompt here" --verbose
```

## Example Calculator App

Included in this project is an example calculator application (in the `calculator/` directory) that demonstrates the capabilities of the AI Code Assistant. The calculator can evaluate mathematical expressions and follows standard operator precedence rules.

To use the calculator directly:

```bash
python calculator/main.py "3 + 5"
```

## License

MIT
