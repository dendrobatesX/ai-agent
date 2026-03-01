import os
from google.genai import types
def get_files_info(working_directory, directory="."):
    try:

        path=os.path.abspath(working_directory)
        full_path=os.path.normpath(os.path.join(path, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([path, full_path]) == path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        content=[]
        for file in os.listdir(full_path):
            file_path=os.path.join(full_path, file)
            size = os.path.getsize(file_path)
            is_directory=os.path.isdir(file_path)

            content.append(
                f"- {file}: file_size={size} bytes, is_dir={is_directory}"
            )
        return "\n".join(content)
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)