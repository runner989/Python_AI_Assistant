import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.call_function import call_function

def main():
    load_dotenv()

    all_args = sys.argv[1:]
    verbose = False
    prompt_list = []

    if all_args and all_args[-1 ] == "--verbose":
        verbose = True
        prompt_list = all_args[:-1]
    else:
        prompt_list = all_args

    if not prompt_list:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(prompt_list)

    if verbose:
        print(f"User prompt: {user_prompt}")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please ensure you have a .env file with GEMINI_API_KEY set or that the variable is otherwise available in your environment.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # Define a system prompt
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    # Define function schemas
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file within the permitted working directory and returns its output.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the Python file to execute, relative to the working directory.",
                ),
            },
            required=["file_path"],
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a file within the permitted working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file to write, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="Content to write to the file.",
                ),
            },
            required=["file_path", "content"],
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads and returns the content of a file within the permitted working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file to read, relative to the working directory.",
                ),
            },
            required=["file_path"],
        ),
    )

    # Create a Tool with all function declarations
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        max_iterations = 20
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            if verbose:
                print(f"\n--- Iteration {iteration} ---")
            
            # Generate a response from the model
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
            
            # Add all candidate responses to the messages
            has_function_call = False
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    messages.append(candidate.content)
                    
                    # Check for function calls in this candidate
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call'):
                            has_function_call = True
                            function_call_part = part.function_call

                            if not function_call_part:
                                if verbose:
                                    print("Warning: Received a null function_call part from the model.")
                                continue

                            # Call the function and get the result
                            function_call_result = call_function(function_call_part, verbose=verbose)
                            
                            # Verify that the function result contains a response
                            if not function_call_result.parts or not hasattr(function_call_result.parts[0], 'function_response') or \
                               not hasattr(function_call_result.parts[0].function_response, 'response'):
                                raise RuntimeError(f"Function call to {function_call_part.name} did not return a valid response")
                            
                            # Add the function result to messages
                            messages.append(function_call_result)
                            
                            # If verbose mode is on, print the function response
                            if verbose:
                                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # If no function calls were made, we're done
            if not has_function_call:
                if response.text:
                    print(response.text)
                break
                
            if iteration >= max_iterations:
                print("Reached maximum number of iterations. Stopping.")
                break
                
        if verbose and response.usage_metadata:
            print(f"\nToken usage for last request:")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
