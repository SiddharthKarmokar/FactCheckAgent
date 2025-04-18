import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

projectName = "project"

list_of_files = [
    ".github/workflow/.gitkeep",
    f"src/{projectName}/components/__init__.py",
    f"src/{projectName}/components/logging/__init__.py",
    ".gitignore",
    "app.py",
    "main.py",
    "Dockerfile",
    "requirements.txt",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    if (not os.path.exists(filepath) or (os.path.getsize(filepath) == 0)):
        with open(filepath, 'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} already exists")
