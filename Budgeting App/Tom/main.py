import hashlib
import json

from pprint import pprint

path = ".\\Budgeting App\\Tom\\"
budget_data = {}

def hash_password(password):
    """Return the SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()


def login(username, password):
    print("Logging in")

    # Read usernames
    with open(path + "usernames.txt", "r") as usernames:
        names = [name.strip() for name in usernames]
        usernames.close()

    # Read hashed passwords
    with open(path + "passwords.txt", "r") as passwords:
        passs = [word.strip() for word in passwords]
        passwords.close()

    # Hash the password entered by the user
    hashed_input_password = hash_password(password)

    # Check each stored username/password pair
    for i in range(len(names)):
        if username == names[i] and hashed_input_password == passs[i]:
            return True

    return False


def addUser():
    username = input("Enter a Username: ")
    password = input("Enter Password:   ")

    # Hash password before storing
    hashed_password = hash_password(password)

    with open(path + "passwords.txt", "a") as passes:
        passes.write(f"{hashed_password}\n")
        passes.close()
    with open(path + "usernames.txt", "a") as users:
        users.write(f"{username}\n")
        users.close()

def bubble_sort(arr):
    n = len(arr)
    # Traverse through all elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def printValues():
    with open(f"{path}budget.json", "r") as f:
        d = json.load(f)
        pprint(d)

if __name__ == "__main__":
    LoginRegister = input("Do you have an account? (Yes or No):     ")
    if LoginRegister.lower() == "yes":
        hasLogged = login(input("Enter your Username:     "), input("Enter your Password:     "))
    else:
        print("Please make an account")
        addUser()
        hasLogged = login(input("Enter your Username:     "), input("Enter your Password:     "))
    print("----------------------------------")
    while True:
        if hasLogged:
            income = float(input("Enter your income in pounds.pence:  (no pound sign)"))
            NoOfExpences = int(input("Enter the number of expences: "))
            Food = []
            Travel = []
            Rent = []
            Other = []



            for i in range(NoOfExpences):
                expence = float(input("Enter an cost of expence:  "))
                type = input("Enter the type of expence (Food , Travel, Rent, Other):    ")
                type.lower()
                match type:
                    case "food":
                        Food.append(expence)
                    case "travel":
                        Travel.append(expence)
                    case "rent":
                        Rent.append(expence)
                    case _:
                        Other.append(expence)


            with open(f"{path}budget.json", "r") as f:
                try:
                    budget_data = json.load(f)
                    if budget_data == {}:
                        budget_data = {
                            "Income": 0,
                            "Food": [],
                            "Travel": [],
                            "Rent": [],
                            "Other": []
                        }
                except json.JSONDecodeError:
                    budget_data = {"Income": 0, "Food": [], "Travel": [], "Rent": [], "Other": []}
            budget_data["Income"] = income
            budget_data["Food"].extend(Food)
            budget_data["Travel"].extend(Travel)
            budget_data["Rent"].extend(Rent)
            budget_data["Other"].extend(Other)
            with open(f"{path}budget.json", "w") as f:
                json.dump(budget_data, f, indent=4)

            with open(f"{path}budget.json", "r") as f:
                data = json.load(f)
                for values in data:
                    for items in data[values]:
                        if values == "Income":
                            total = data[values]
                        else:
                            total = total - items
                    print(f"Your Total Budget left is {total}")



