import os
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