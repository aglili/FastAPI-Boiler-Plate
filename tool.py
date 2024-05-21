#!/usr/bin/env python3

import os 
import shutil

BOILERPLATE_PATH = os.path.join(os.path.dirname(__file__), "app")

def init():
    """
    Initializes a new FastAPI project with the given project name.

    This function prompts the user to enter a project name and creates a new folder with that name in the current working directory. If a folder with the same name already exists, it prints a message and returns.

    The function then copies all the files and directories from the `BOILERPLATE_PATH` directory to the newly created project folder.

    Parameters:
        None

    Returns:
        None
    """
    
    print("Initialize your FastAPI project")
    project_name = input("Project Name: ")
    
    folder = os.path.join(os.getcwd(), project_name)
    if os.path.exists(folder):
        print("A folder with such name already exists")
        return

    os.makedirs(folder)
    
    for root, dirs, files in os.walk(BOILERPLATE_PATH):
        for file in files:
            src = os.path.join(root, file)
            directory = os.path.join(folder, os.path.relpath(src, BOILERPLATE_PATH))
            os.makedirs(os.path.dirname(directory), exist_ok=True)
            shutil.copy(src, directory)

    print("Project created successfully")

if __name__ == "__main__":
    init()