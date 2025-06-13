import os


def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(file_path)

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        try:
            with open(abs_file_path, 'w') as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except PermissionError:
            return f'Error: Permission denied writing to file: "{file_path}"'
        except IOError as e:
            return f'Error: IO error while writing file: "{file_path}" - {str(e)}'
    except Exception as e:
        return f'Error: Unexpected error: {str(e)}'
