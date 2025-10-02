import time

def GenNewPassword(NUC: int, NLC: int, NI: int, NS: int, TotalLength: int):
    """********Details about these parameters********\n
        NUC :- mininum number of upper case characters\n
        NLC :- mininum number of lower case characters\n
        NI :- mininum number of Numbers\n
        NS :- mininum number of symbol\n
        TotalLength :- total length of your password
        """
    import secrets
    NUMS = "1234567890"
    ALPHA_U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ALPHA_L = ALPHA_U.lower()
    SYMBOLS = "!@#$%^&*|/?.~:;'+=-_"
    ALL = NUMS + ALPHA_U + ALPHA_L + SYMBOLS

    result = []

    # minimum requirements
    result += [secrets.choice(NUMS) for _ in range(NI)]
    result += [secrets.choice(ALPHA_U) for _ in range(NUC)]
    result += [secrets.choice(ALPHA_L) for _ in range(NLC)]
    result += [secrets.choice(SYMBOLS) for _ in range(NS)]

    # fill remaining
    remaining = TotalLength - len(result)
    result += [secrets.choice(ALL) for _ in range(remaining)]

    # shuffle securely
    secrets.SystemRandom().shuffle(result)

    return ''.join(result)


def takeInputs():
    y = input("Do you want to generate a password(y/n): ").lower().strip()
    if y == "y":
        MUC = input("Enter mininum number of upper case letters: ")
        MLC = input("Enter mininum number of lower case letters: ")
        MI = input("Enter mininum number of numbers: ")
        MS = input("Enter mininum number of symbols: ")
        TL = input("Enter maximum length of password: ")

        try:
            MUC = int(MUC)
            MLC = int(MLC)
            MI = int(MI)
            MS = int(MS)
            TL = int(TL)
            return [MUC, MLC, MI, MS, TL]
        except Exception:
            print("Only enter numbers!")
            print("Program closed due to error!")
            time.sleep(2)
            return None
    elif y == "n":
        print("Exiting...")
        time.sleep(2)
        print("Program closed!")
        time.sleep(1)
        return None
    else:
        print("Wrong Input; choose (y/n) only!")
        print("Program closed due to error!")
        time.sleep(2)
        return None

def main():

    while True:
        Inputs = takeInputs()
        if Inputs == None:
            break
        else:
            password = GenNewPassword(Inputs[0], Inputs[1], Inputs[2], Inputs[3], Inputs[4])
            print("Your required password is generated => ", password)
            print()

if __name__ == "__main__":
    main()
