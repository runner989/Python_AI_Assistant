import os
import subprocess
import sys


def run_python_file(working_directory, file_path):
    try:
        # Convert paths to absolute paths
        abs_working_dir = os.path.abspath(working_directory)

        # Handle the case where file_path is already absolute
        if os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            # For relative paths, join with working directory
            abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

        # Check if file is within working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found'

        # Check if file is a Python file
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        # Execute the Python file with subprocess
        try:
            process = subprocess.run(
                [sys.executable, abs_file_path],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.path.dirname(abs_file_path)
            )

            # Format the output
            output = []

            # Add stdout if it exists
            if process.stdout:
                output.append(f"STDOUT:\n{process.stdout.strip()}")

            # Add stderr if it exists
            if process.stderr:
                output.append(f"STDERR:\n{process.stderr.strip()}")

            # Add exit code if non-zero
            if process.returncode != 0:
                output.append(f"Process exited with code {process.returncode}")

            # Return formatted output or "No output" message
            if output:
                return "\n\n".join(output)
            else:
                return "No output produced."

        except subprocess.TimeoutExpired:
            return "Error: Process timed out after 30 seconds"

    except Exception as e:
        return f"Error: executing Python file: {e}"
