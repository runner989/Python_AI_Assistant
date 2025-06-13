import os
import os.path


def get_file_content(working_directory, file_path):
    try:
        try:
            abs_working_dir = os.path.abspath(working_directory)
            abs_file_path = os.path.abspath(file_path)
        except Exception as e:
            return f'Error: Failed to resolve file path: {str(e)}'

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        try:
            if not os.path.isfile(abs_file_path):
                return f'Error: File not found or is not a regular file: "{file_path}"'

            with open(abs_file_path, 'r') as file:
                content = file.read()
                if len(content) > 10000:
                    content = content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'
                return content
        except PermissionError:
            return f'Error: Permission denied accessing file: "{file_path}"'
        except UnicodeDecodeError:
            return f'Error: Unable to decode file contents: "{file_path}"'
        except IOError as e:
            return f'Error: IO error while reading file: "{file_path}" - {str(e)}'
    except Exception as e:
        return f'Error: Unexpected error: {str(e)}'
