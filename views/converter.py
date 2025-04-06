import os
import subprocess

UI_DIR = "views/ui"
PY_DIR = "views/py"

""""
Converted ui files:
    loginScreen

"""

# Files you want to convert (just base names, no extension)
selected_files = ["mainDashboard"]

os.makedirs(PY_DIR, exist_ok=True)

for base_name in selected_files:
    ui_path = os.path.join(UI_DIR, f"{base_name}.ui")
    py_path = os.path.join(PY_DIR, f"{base_name}.py")

    if not os.path.exists(ui_path):
        print(f"⚠ File not found: {ui_path}")
        continue

    cmd = ["pyside6-uic", ui_path, "-o", py_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✔ Converted: {ui_path} → {py_path}")
    else:
        print(f"❌ Failed to convert {ui_path}:\n{result.stderr}")
