import os
import subprocess

# Paths
UI_DIR = "views/ui"
PY_DIR = "views/py"

# Ensure output directory exists
os.makedirs(PY_DIR, exist_ok=True)

# Convert all .ui files
for filename in os.listdir(UI_DIR):
    if filename.endswith(".ui"):
        ui_path = os.path.join(UI_DIR, filename)
        base_name = os.path.splitext(filename)[0]
        py_path = os.path.join(PY_DIR, f"{base_name}.py")

        # Run the PySide6 UI Compiler
        cmd = ["pyside6-uic", ui_path, "-o", py_path]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✔ Converted: {filename} → {py_path}")
        else:
            print(f"❌ Failed to convert {filename}:\n{result.stderr}")
