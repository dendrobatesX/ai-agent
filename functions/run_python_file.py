import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    try:
        path=os.path.abspath(working_directory)
        full_path=os.path.normpath(os.path.join(path, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([path, full_path]) == path
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_path]
        if not args==None:
            command.extend(args)

        response=subprocess.run(command, cwd=path, capture_output=True, timeout=30, text=True)
        output_lines=[]

        if not response.returncode==0:
            output_lines.append(f"Process exited with code {response.returncode}")
        if response.stdout:
            output_lines.append(f"STDOUT:\n{response.stdout}")
        if response.stderr:
            output_lines.append(f"STDERR:\n{response.stderr}")
        if not response.stdout and not response.stderr:
            output_lines.append("No output produced")
        return "\n".join(output_lines)

        
    except Exception as e:
        return f"Error: executing Python file: {e}"