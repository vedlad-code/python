import os
from pathlib import Path
import subprocess
import sys



def resolve_path(rawPath):
    return Path(rawPath).expanduser().resolve()

current_dir = Path.home()

def change_dir():
    global current_dir
    rawPath = input("Enter path to navigate to: ")
    new_path = (current_dir / rawPath).expanduser().resolve()
    
    if new_path.is_dir():
        current_dir = new_path
        print(f"Now in: {current_dir}")
    else:
        print("Not a valid directory.")


def file_create():
    rawPath = input("Enter the path of file: ")
    path = (current_dir / rawPath).expanduser().resolve()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        f = open(path, "x")
        f.close()
        print(f"{path} is created.")
    except FileExistsError:
        print("File already exist.")

def dir_create():
    rawPath = input("Enter the path of directory: ")
    path = (current_dir / rawPath).expanduser().resolve()
    try:
        path.mkdir(parents=True, exist_ok=False)
        print(f"{path} is created.")
    except FileExistsError:
        print("Directory already exists.")

def read_file():
    rawPath = input("Enter the path of file: ")
    path = (current_dir / rawPath).expanduser().resolve()
    try:
        print(f"Opening {path}")
        with open(path, "r") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print("File not found.")

def upd_file():
    rawPath = input("Enter the path of file: ")
    path = (current_dir / rawPath).expanduser().resolve()
    try:
        content = input("Write your content: ")
        with open(path, "a") as f:
            f.write("\n", content)
        print(f"{path} is updated.")
    except FileNotFoundError:
        print("File not found.")

def del_file():
    rawPath = input("Enter the path of file: ")
    path = (current_dir / rawPath).expanduser().resolve()
    try:
        os.remove(path)
        print(f"{path} is deleted")
    except FileNotFoundError:
        print("File not found.")

def del_dir():
    rawPath = input("Enter the path of directory: ")
    path = (current_dir / rawPath).expanduser().resolve()
    try:
        path.rmdir()
        print(f"{path} deleted.")
    except FileNotFoundError:
        print(f"{path} does not exist.")
    except OSError:
        print(f"{path} is not empty.")

def lst_dir():
    rawPath = input("Enter the path of directory: ")
    path = (current_dir / rawPath).expanduser().resolve()
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
    path = (current_dir / rawPath).expanduser().resolve()
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
    print(f"Current directory: {current_dir}")
    try:
        task = int(input('''Choose your task:
1. Create a new file
2. Read a file
3. Update an exsisting file
4. Delete a file
5. Make a directory
6. Delete directory
7. Navigate to directory
8. Open a file
9. List directory content
10. Quit
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
        change_dir() 
    elif task == 8:
        open_file()
    elif task == 9:
        lst_dir()
    elif task == 10:
        print("Quitting program.")
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        break
    else:
         print("Invalid input.")
