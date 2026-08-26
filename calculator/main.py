running = True

while running:
    num1 = int(input("Enter 1st number: "))
    num2 = int(input("Enter 2nd number: "))
    oprator = input("Available operators: +, -, *, / : ")

    if oprator == "+":
        print(f"{num1} + {num2} = {num1 + num2}")
    elif oprator == "-":
        print(f"{num1} - {num2} = {num1 - num2}")
    elif oprator == "*":
        print(f"{num1} * {num2} = {num1 * num2}")
    elif oprator == "/":
        if num2 != 0:
            print(f"{num1} / {num2} = {num1 / num2}")
        else:
            print("Cannot divide by 0")

    conti = input("Do you want to continue?: ")
    if conti != "yes":
        print("Quiting program...")
        running = False