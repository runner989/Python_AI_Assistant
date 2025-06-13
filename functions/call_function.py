from google.genai import types
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
import json
import os

def call_function(function_call_part, verbose=False):
    """
    Call a function based on the function call part from the LLM response.
    
    Args:
        function_call_part: types.FunctionCall with name and args
        verbose: If True, print detailed function call information
        
    Returns:
        types.Content with the function response or error message
    """
    function_name = function_call_part.name
    
    # Print function call information based on verbosity
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Map of available functions
    available_functions = {
        'get_files_info': get_files_info,
        'run_python_file': run_python_file,
        'write_file': write_file,
        'get_file_content': get_file_content
    }
    
    # Check if function exists
    if function_name not in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Get the function to call
    function_to_call = available_functions[function_name]
    
    try:
        # Parse arguments
        if isinstance(function_call_part.args, dict):
            args_dict = function_call_part.args.copy()  # Create a copy to avoid modifying the original
        else:
            try:
                args_dict = json.loads(function_call_part.args)
            except json.JSONDecodeError:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"error": f"Invalid JSON in function arguments: {function_call_part.args}"},
                        )
                    ],
                )
        
        # Set working directory based on function
        if function_name == 'get_files_info':
            # For get_files_info, use the specified directory or default to working_directory
            if 'directory' not in args_dict or not args_dict['directory']:
                args_dict['directory'] = './calculator'
            elif not any(args_dict['directory'].startswith(p) for p in ('./calculator/', 'calculator/')):
                # If directory is specified but not in calculator, prepend working_directory
                args_dict['directory'] = os.path.join('./calculator', args_dict['directory'].lstrip('/'))
            args_dict['working_directory'] = './calculator'
        else:
            # For other functions, set working_directory and handle file paths
            args_dict['working_directory'] = './calculator'
            if function_name in ['get_file_content', 'write_file'] and 'file_path' in args_dict:
                file_path = args_dict['file_path']
                if not file_path.startswith(('./calculator/', 'calculator/')):
                    args_dict['file_path'] = os.path.join('./calculator', file_path.lstrip('/'))
        
        # Call the function with the provided arguments
        function_result = function_to_call(**args_dict)
        
        # Return the successful response
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
        
    except Exception as e:
        # Handle any exceptions that occur during function execution
        error_message = str(e)
        if verbose:
            print(f"Error calling {function_name}: {error_message}")
            
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error calling {function_name}: {error_message}"},
                )
            ],
        )
