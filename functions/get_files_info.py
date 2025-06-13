import os
import subprocess


# If any errors are raised by the standard library functions, catch them and instead return a string describing the error. Always prefix error strings with "Error:"
def get_files_info(working_directory, directory=None):
    try:
        if directory:
            try:
                target_dir = os.path.abspath(directory)
                working_dir = os.path.abspath(working_directory)
                if not target_dir.startswith(working_dir):
                    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
                if not os.path.isdir(target_dir):
                    return f'Error: "{directory}" is not a directory'
            except Exception as e:
                return f'Error: Failed to validate directory path: {str(e)}'
        else:
            try:
                target_dir = os.path.abspath(working_directory)
            except Exception as e:
                return f'Error: Failed to resolve working directory path: {str(e)}'

        entries = []
        try:
            for entry in os.listdir(target_dir):
                try:
                    entry_path = os.path.join(target_dir, entry)
                    is_dir = os.path.isdir(entry_path)
                    size = 0 if is_dir else os.path.getsize(entry_path)
                    entries.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
                except Exception as e:
                    entries.append(f"- {entry}: Error: Failed to get file info: {str(e)}")
            return "\n".join(entries)
        except Exception as e:
            return f"Error: Failed to list directory contents: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error: {str(e)}"
