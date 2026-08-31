import secrets

running = True
i = 0
choiceList = ["rock", "paper", "scissor"]

while running and i<6:
    print("Rock Paper Scissors")
    userChoice = input(": ")
    compChoice = secrets.choice(choiceList)
    if userChoice != "quit":
        print(f"{userChoice} : {compChoice}")
        if userChoice == compChoice:
            print("draw")
        elif  userChoice.lower() == "rock" and compChoice == "paper":
            print("comp wins")
        elif userChoice.lower() == "rock" and compChoice == "scissor":
            print("user wins")
        elif userChoice.lower() == "paper" and compChoice == "rock":
            print("user wins")
        elif userChoice.lower() == "paper" and compChoice == "scissor":
            print("comp wins")
        elif userChoice.lower() == "scissor" and compChoice == "paper":
            print("user wins")
        elif userChoice.lower() == "scissor" and compChoice == "rock":
            print("comp wins")
    else:
        break