import subprocess
import os

# get current folder
current_dir = os.path.dirname(os.path.abspath(__file__))

# path to app.py
app_path = os.path.join(current_dir, "app.py")

# run streamlit
subprocess.run([
    "streamlit",
    "run",
    app_path
])