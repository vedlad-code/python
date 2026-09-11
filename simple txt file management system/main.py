import os
import pathlib as Path

def file_create():
    rawPath = input("Enter the path of file.")
    path = path("Home")/rawPath
    # fileName = input("Enter file name: ")
    # dirName = input("You want to make this file in which directory? ")

    # if dirName.lower() == "home":
    #     path = Path("Home")/f"{fileName}.txt"
    # else:
    #     path = Path("Home")/dirName/f"{fileName}.txt"

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        f = open(path, "x")
        f.close()
        print(f"{path} is created.")
    except FileExistsError:
        print("File already exist")
        
running = True

while running:
    print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
    print("TXT MANAGER - Create and manage txt files")
    task = int(input('''Choose your task:
1. Create a new file
2. Read a file
3. Update an exsisting file
4. Overwrite a file
5. Delete a file or directory
6. Make a directory
7. Delete directory
8. List directory content
10. Quit
: '''))

    if task == 1:
        file_create()
    elif task == 2:
        name = input("Enter file name: ")
        try:
            print(f"Opening {name}.txt")
            with open(f"Home/{name}.txt", "r") as f:
                content = f.read()
                print(content)
        except FileNotFoundError:
            print("File not found")
    elif task == 3:
        name = input("Enter file name: ")
        try:
            content = input("Write your content: ")
            with open(f"Home/{name}.txt", "a") as f:
                f.write(content)
            print(f"{name}.txt is updated")
        except FileNotFoundError:
            print("File not found")
    elif task == 4:
        name = input("Enter file name: ")
        try:
            content = input("Write your content: ")
            with open(f"Home/{name}.txt", "w") as f:
                f.write(content)
            print(f"{name}.txt is overwritten")
        except FileNotFoundError:
            print("File not found")
    elif task == 5:
        quest = input("What do you want to delete, file or directory")
        if quest.lower() == "file":
            fileName = input("Enter file name: ")
            try:
                os.remove(f"Home/{name}.txt")
                print(f"{name}.txt is deleted")
            except FileNotFoundError:
                print("File not found")
    elif task == 6:
        nameDir = input("Name the directory: ")
        try:
            os.mkdir(f"Home/{nameDir}")
        except FileExistsError:
            print("Directory already exists")
    elif task == 7:
        nameDir = input("Enter directory name: ")
        try:
            os.rmdir(f"Home/{nameDir}")
            print("Directory deleted.")
        except FileNotFoundError:
            print("Directory doesn't exist.")
        except OSError:
            print("Directory is not empty!")
    elif task == 8:
        nameDir = input("Enter directory name: ")
        try:
            print(f"Showing {nameDir}")
            print(os.listdir(nameDir))
        except FileNotFoundError:
            print("Directory doesn't exist")

    elif task == 10:
        print("Quitting program")
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        break
    else:
         print("Invalid input")
