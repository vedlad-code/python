# imports
import math
import secrets

# lists
ucaseChar = [chr(i) for i in range(65, 91)]
lcaseChar = [chr(i) for i in range(97, 123)]
digits = [chr(i) for i in range(48, 58)]
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']']

# main code
running = True

while running:
    choice = input("""What do you want to do.
1. Generate Password
2. Check Password Strength
3. Quit \n
YOUR CHOICE: """)
    if choice == "1":
        # generated password
        genPass = ""
        bigPool = ucaseChar+lcaseChar+digits+symbols
        for i in range(18):
            genPass += secrets.choice(bigPool)
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        print(f"Your generated password is: {genPass}")
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")

    elif choice == "2":
        # inputs
        password = input("Enter your password: ")

        

        # common pass list
        with open("commonPasses.txt", "r") as f:
            commonPasswords = set(line.strip() for line in f)

        # variables
        uCount = 0
        lCount = 0
        symCount = 0
        digiCount = 0

        passLength = len(password)

        poolSize = 0
        patternpts = 0
        entropy = 0

        for i in range(passLength):
            if password[i] in ucaseChar:
                uCount += 1
            elif password[i] in lcaseChar:
                lCount += 1
            elif password[i] in digits:
                digiCount += 1
            elif password[i] in symbols:
                symCount += 1

        # pattern points checks

        # repeating character check
        for i in range(passLength - 3):
            if password[i] == password[i+1] == password[i+2] == password[i+3]:
                patternpts += 1

        # sequential character check
        for i in range(passLength - 2):
            diff1 = ord(password[i+1]) - ord(password[i])
            diff2 = ord(password[i+2]) - ord(password[i+1])
            if diff1 == diff2 and (diff1 == 1 or diff1 == -1):
                patternpts += 1

        # keyboard sequence check
        keyRows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

        for row in keyRows:
            for i in range(passLength - 2):
                pos0 = row.find(password[i])
                pos1 = row.find(password[i+1])
                pos2 = row.find(password[i+2])

                if pos0 != -1 and pos1 != -1 and pos2 != -1:
                    diff1 = pos1 - pos0
                    diff2 = pos2 - pos1
                    if diff1 == diff2 and (diff1 == 1 or diff1 == -1):
                        patternpts += 1

        # common password check
        passwordLower = password.lower()

        if passwordLower in commonPasswords:
            patternpts += 1
        else:
            for common in commonPasswords:
                if common in passwordLower:
                    patternpts += 1
                    break

        # entropy calculation
        if lCount > 0:
            poolSize += 26
        if uCount > 0:
            poolSize += 26
        if symCount > 0:
            poolSize += 16
        if digiCount > 0:
            poolSize += 10

        if poolSize == 0 or passLength == 0:
            entropy = 0
        else:
            entropy = passLength * math.log2(poolSize)

        # entropy normalisation
        effectiveEntropy = entropy - (patternpts * 10)
        effectiveEntropy = max(0, effectiveEntropy)

        # result
        if effectiveEntropy < 28:
            strength = "very weak"
        elif effectiveEntropy < 36:
            strength = "weak"
        elif effectiveEntropy < 60:
            strength = "reasonable"
        elif effectiveEntropy < 128:
            strength = "strong"
        else:
            strength = "very strong"

        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        print(f"Your password strength is {strength}")
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")

    elif choice == "3":
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        print("Quitting program")
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        running = False

    else:
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        print("Invalid choice")
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
