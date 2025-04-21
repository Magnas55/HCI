import sys
import io
import os
from datetime import datetime

def save_code_version(code_input):
    path = "versions/auto"
    os.makedirs(path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{path}/code_{timestamp}.py"
    with open(filename, "w") as f:
        f.write(code_input)


def save_named_version(code_input, name):
    path = "versions/saved"
    os.makedirs(path, exist_ok=True)

    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"{path}/{safe_name}.py"

    existing_versions = [f for f in os.listdir(path) if f.endswith(".py")]

    if len(existing_versions) >= 5:
        return False, "Version limit reached (max 5). Delete older versions first."

    if os.path.exists(filename):
        return False, f"A version named '{safe_name}' already exists."

    with open(filename, "w") as f:
        f.write(code_input)

    return True, f"Version '{safe_name}' saved successfully."


def run_code(code_input, output_window, var_window):
    try:
        save_code_version(code_input)  # <-- Save version before running

        old_stdout = sys.stdout
        sys.stdout = output_buffer = io.StringIO()

        local_vars = {}
        exec(code_input, {}, local_vars)

        sys.stdout = old_stdout
        output_window.update(output_buffer.getvalue())

        var_display = "\n".join([f"{k}: {v}" for k, v in local_vars.items()])
        var_window.update(var_display if var_display else "No variables.")
    except Exception as e:
        sys.stdout = old_stdout
        output_window.update(f"Error: {e}")


def list_named_versions():
    path = "versions/saved"
    os.makedirs(path, exist_ok=True)
    return sorted(f for f in os.listdir(path) if f.endswith(".py"))

def load_named_version(name):
    path = f"versions/saved/{name}"
    with open(path, "r") as f:
        return f.read()
    
def delete_named_version(name):
    path = f"versions/saved/{name}"
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
