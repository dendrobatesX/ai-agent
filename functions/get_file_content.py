import os
def get_file_content(working_directory, file_path):
    try:
        path=os.path.abspath(working_directory)
        full_path=os.path.normpath(os.path.join(path, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([path, full_path]) == path
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{full_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
        
    except Exception as e:
        return f"Error: {str(e)}"