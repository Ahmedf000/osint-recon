import subprocess
from sherlock_project import *

def check_user(username):
    process = subprocess.run(
        ["sherlock", username, "--print-found"],
        capture_output=True,
        text=True
    )
    return process.stdout

