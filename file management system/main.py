import os
from pathlib import Path
import subprocess
import sys

def file_create():
    rawPath = input("Enter the path of file: ")
    path = Path("Home")/rawPath
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        f = open(path, "x")
        f.close()
        print(f"{path} is created.")
    except FileExistsError:
        print("File already exist.")

def dir_create():
    rawPath = input("Enter the path of directory: ")
    path = Path("Home") / rawPath
    try:
        path.mkdir(parents=True, exist_ok=False)
        print(f"{path} is created.")
    except FileExistsError:
        print("Directory already exists.")

def read_file():
    rawPath = input("Enter the path of file: ")
    path = Path("Home")/rawPath
    try:
        print(f"Opening {path}")
        with open(path, "r") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print("File not found.")

def upd_file():
    rawPath = input("Enter the path of file: ")
    path = Path("Home")/rawPath
    try:
        content = input("Write your content: ")
        with open(path, "a") as f:
            f.write(content)
        print(f"{path} is updated.")
    except FileNotFoundError:
        print("File not found.")

def del_file():
    rawPath = input("Enter the path of file: ")
    path = Path("Home")/rawPath
    try:
        os.remove(path)
        print(f"{path} is deleted")
    except FileNotFoundError:
        print("File not found.")

def del_dir():
    rawPath = input("Enter the path of directory: ")
    path = Path("Home")/rawPath
    try:
        path.rmdir()
        print(f"{path} deleted.")
    except FileNotFoundError:
        print(f"{path} does not exist.")
    except OSError:
        print(f"{path} is not empty.")

def lst_dir():
    rawPath = input("Enter the path of directory: ")
    path = Path("Home")/rawPath
    try:
        print(f"Showing {path}")
        for item in path.iterdir():
            print(item)
    except FileNotFoundError:
        print("Directory doesn't exist.")
    except NotADirectoryError:
        print(f"{path} is not a directory.")

def open_file():
    rawPath = input("Enter the path of file: ")
    path = Path("Home") / rawPath
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", path])
        elif sys.platform == "win32":
            os.startfile(path)
        else:
            subprocess.run(["xdg-open", path])
        print(f"Opening {path}")
    except FileNotFoundError:
        print("File not found.")


running = True

while running:
    print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
    print("TXT MANAGER - Create and manage txt files")
    try:
        task = int(input('''Choose your task:
1. Create a new file
2. Read a file
3. Update an exsisting file
4. Delete a file
5. Make a directory
6. Delete directory
7. List directory content
8. Open a file
9. Quit
: '''))
    except ValueError:
        print("please enter valid number.")
        continue

    if task == 1:
        file_create()
    elif task == 2:
        read_file()
    elif task == 3:
        upd_file()
    elif task == 4:
        del_file()
    elif task == 5:
        dir_create()
    elif task == 6:
        del_dir()  
    elif task == 7:
        lst_dir()
    elif task == 8:
        open_file()
    elif task == 9:
        print("Quitting program.")
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        break
    else:
         print("Invalid input.")
