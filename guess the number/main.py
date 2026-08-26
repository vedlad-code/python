import random

randNum = random.randint(1, 100)
running = True

while running:
    guessNum = int(input("Guess a number between 1 to 100: "))

    if guessNum == randNum:
        print("Your guess is correct...")
        conti = input("Do you want to replay? : ")
        if conti != "yes":
            print("Quitting program...")
            break
        else:
            randNum = random.randint(1, 100)

    else:
        if guessNum > randNum:
            print("Your guess is high.")
        else:
            print("Your guess is low.")
