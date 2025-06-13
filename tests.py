import os
from functions.run_python import run_python_file


def main():
    # Make sure we're running from the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    print("\nTest 1: run_python_file('calculator', 'main.py')")
    result = run_python_file("calculator", "main.py")
    print(f"Result: {result}")

    print("\nTest 2: run_python_file('calculator', 'tests.py')")
    result = run_python_file("calculator", "tests.py")
    print(f"Result: {result}")

    print("\nTest 3: run_python_file('calculator', '../main.py')")
    result = run_python_file("calculator", "../main.py")
    print(f"Result: {result}")

    print("\nTest 4: run_python_file('calculator', 'nonexistent.py')")
    result = run_python_file("calculator", "nonexistent.py")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
