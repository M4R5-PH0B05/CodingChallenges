# Imports
import psycopg2
import hashlib

# Variables and Constants
loginChoice = None
actionChoice = None

username = None
password = None
email = None
user_id = None  # Track the logged-in user's ID
login = False

registerEmail = None
registerUsername = None
registerPassword = None


# Functions
def hash_password(password):
    """Create a new hash for each password"""
    return hashlib.sha256(password.encode()).hexdigest()


class database:
    def __init__(self):
        self.DB_NAME = "budgetapp"
        self.DB_USER = "mars"
        self.DB_PASS = "Morgan1206!"
        self.DB_HOST = "100.118.16.69"
        self.DB_PORT = "32768"
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(database=self.DB_NAME,
                                         user=self.DB_USER,
                                         password=self.DB_PASS,
                                         host=self.DB_HOST,
                                         port=self.DB_PORT)
            print("Database connection established")
            return True

        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    def register(self, username, password, email):
        try:
            cur = self.conn.cursor()
            # Use parameterized queries to prevent SQL injection
            cur.execute("""
                        INSERT INTO users (username, password, email)
                        VALUES (%s, %s, %s)
                        """, (username, password, email))
            self.conn.commit()
            print("Registered successfully")
            return True
        except Exception as e:
            print(f"Failed to register: {e}")
            return False

    def getInfo(self, username):
        cur = self.conn.cursor()
        # Use parameterized queries to prevent SQL injection
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        data = cur.fetchall()
        return data

    def close(self):
        if self.conn:
            self.conn.close()

    def addExpense(self, id, expense, date, category):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                        INSERT INTO expenses (id, expense, date, category)
                        VALUES (%s, %s, %s, %s)
                        """, (id, expense, date, category))
            self.conn.commit()
            print("Expense added successfully!")
            return True
        except Exception as e:
            print(f"Failed to add expense: {e}")
            return False

    def addIncome(self, id, income, date, category):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                        INSERT INTO incomes (id, income, date, note)
                        VALUES (%s, %s, %s, %s)
                        """, (id, income, date, category))
            self.conn.commit()
            print("Income added successfully!")
            return True

        except Exception as e:
            print(f"Failed to add income: {e}")
            return False

    def returnExpenses(self, id):
        cur = self.conn.cursor()
        # Use parameterized queries to prevent SQL injection
        cur.execute("SELECT * FROM expenses WHERE id = %s", (id,))
        data = cur.fetchall()
        return data

    def returnIncomes(self, id):
        cur = self.conn.cursor()
        # Use parameterized queries to prevent SQL injection
        cur.execute("SELECT * FROM incomes WHERE id = %s", (id,))
        data = cur.fetchall()
        return data


def display_expenses(expenses):
    """Helper function to display expenses in a consistent format"""
    print("--")
    print("")
    for item in expenses:
        print(f'''Amount: - £{item[1]}
Date: {item[2]}
Category: {item[3]}
--''')
    print("")


# Main body
# Welcome message
print('''
Welcome to SPARE CHANGE ™ Budgeting Software
--
''')

# Create database connection once
data = database()
if not data.connect():
    print("Cannot continue without database connection. Exiting...")
    exit(1)

# login loop
while not login:  # Continue until login is successful
    print('''
Would you like to:
( 1 ) Register 
( 2 ) Login
    ''')

    try:
        loginChoice = float(input("Choice: "))
    except ValueError:
        print("Invalid choice. Please enter 1 or 2.")
        continue

    # register option
    if loginChoice == 1:
        registerUsername = input("Username: ")
        registerPassword = input("Password: ")
        registerEmail = input("Email: ")
        if data.register(registerUsername, hash_password(registerPassword), registerEmail):
            # Get the newly registered user's info
            info = data.getInfo(registerUsername)
            if info:
                user_id = info[0][0]  # Assuming ID is the first column
                username = registerUsername
                login = True

    # login option
    elif loginChoice == 2:
        loginUsername = input("Username: ")
        info = data.getInfo(loginUsername)

        if len(info) < 1:
            print("No account exists with that username. Please try again.")
        else:
            passwordHash = info[0][2]  # stored hash from database
            loginPassword = input("Password: ")
            hashedInputPassword = hash_password(loginPassword)

            if hashedInputPassword == passwordHash:
                print("Login successful!")
                user_id = info[0][0]  # Get user ID from database
                username = loginUsername
                login = True
            else:
                print("Username or password incorrect. Please try again.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

# main app loop
print(f"\nWelcome, {username}!")
while login:
    print("")
    print("Please choose an action from the list below: ")
    print("( 1 ) Add an Expense ")
    print("( 2 ) Add Income ")
    print("( 3 ) View Expenses ")
    print("( 4 ) View Incomes ")
    print("( 5 ) View Whole Account ")
    print("( 6 ) Quit")
    print("")

    try:
        actionChoice = int(input("Choice: "))
    except ValueError:
        print("Invalid choice. Please enter a number.")
        continue

    # add expense
    if actionChoice == 1:
        try:
            expense_amount = float(input("Expense: £"))
            expense_category = input("Category: ")
            expense_date = input("Date (YYYY-MM-DD): ")
            data.addExpense(user_id, expense_amount, expense_date, expense_category)
        except ValueError:
            print("Invalid expense amount. Please enter a number.")
        except Exception as e:
            print(f"Error adding expense: {e}")

    # add income
    elif actionChoice == 2:
        try:
            income_amount = float(input("Income: £"))
            income_date = input("Date (YYYY-MM-DD): ")
            income_note = input("Optional Note: ")
            data.addIncome(user_id, income_amount, income_date, income_note)
        except ValueError:
            print("Invalid income amount. Please enter a number.")
        except Exception as e:
            print(f"Error adding income: {e}")

    # view expenses
    elif actionChoice == 3:
        while True:
            expenses = data.returnExpenses(user_id)

            if not expenses:
                print("No expenses found for your account.")
                break

            # Display all expenses first
            display_expenses(expenses)

            # Get unique categories for filtering
            categories = list(set([item[3] for item in expenses]))

            print('''( 1 ) Sorting Options
( 2 ) Exit
    ''')

            try:
                choice = int(input("Choice: "))
            except ValueError:
                print("Invalid choice. Please enter a number.")
                continue

            if choice == 1:
                print(f"( 1 ) Filter by Category - Available: {', '.join(categories)}")
                print("( 2 ) Sort Lowest to Highest")
                print("( 3 ) Sort Highest to Lowest")
                print("")

                try:
                    sort_choice = int(input("Choice: "))
                except ValueError:
                    print("Invalid choice. Please enter a number.")
                    continue

                if sort_choice == 1:
                    # Filter by category
                    sortBy = input("Enter category name: ")
                    filtered_expenses = [item for item in expenses if item[3].lower() == sortBy.lower()]

                    if filtered_expenses:
                        print(f"\nExpenses in category '{sortBy}':")
                        display_expenses(filtered_expenses)
                    else:
                        print(f"No expenses found in category '{sortBy}'")

                    input("Press ENTER to continue...")

                elif sort_choice == 2:
                    # Sort lowest to highest (by amount - index 1)
                    sorted_expenses = sorted(expenses, key=lambda x: x[1])
                    print("\nExpenses sorted from Lowest to Highest:")
                    display_expenses(sorted_expenses)
                    input("Press ENTER to continue...")

                elif sort_choice == 3:
                    # Sort highest to lowest (by amount - index 1)
                    sorted_expenses = sorted(expenses, key=lambda x: x[1], reverse=True)
                    print("\nExpenses sorted from Highest to Lowest:")
                    display_expenses(sorted_expenses)
                    input("Press ENTER to continue...")

                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")

            elif choice == 2:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    # view incomes
    elif actionChoice == 4:
        incomes = data.returnIncomes(user_id)
        print("--")
        print("")
        for item in incomes:
            print(f'''Amount: + £{item[1]}
Date: {item[2]}
Note: {item[3]}
--''')
        print("")
        input("Press ENTER to continue...")

    # whole account
    elif actionChoice == 5:
        expenses = data.returnExpenses(user_id)
        print("")
        print("EXPENSES")
        print("--")
        for item in expenses:
            print(f'''Amount: - £{item[1]}
Date: {item[2]}
Category: {item[3]}
--''')
        print("")
        incomes = data.returnIncomes(user_id)
        print("INCOMES")
        print("--")
        for item in incomes:
            print(f'''Amount: + £{item[1]}
Date: {item[2]}
Note: {item[3]}
--''')

        # Calculate totals
        total_expenses = sum([item[1] for item in expenses])
        total_income = sum([item[1] for item in incomes])
        balance = total_income - total_expenses

        print(f"Total Expenses: -£{total_expenses:.2f}")
        print(f"Total Income: +£{total_income:.2f}")
        print(f"Current Balance: £{balance:.2f}")
        print("--")

        input("Press ENTER to continue...")

    # quit
    elif actionChoice == 6:
        print("Thank you for using SPARE CHANGE ™!")
        login = False
        data.close()
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")