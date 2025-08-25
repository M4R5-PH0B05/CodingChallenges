# Database > API > Logic > Frontend

# IMPORTS
import psycopg2 as db

# FUNCTIONS
class database:
    self.connection = db.connect(
    database="Finance Dashboard",
    user="mars",
    password="Morgan1206!",
    host="100.118.16.69",
    port="32768")
    self.cursor = self.connection.cursor()

    # USERS
    def register_user(self,first_name,last_name,username,email,password):
        try:
            self.cursor.execute("INSERT INTO users (first_name,last_name,username,email,password) VALUES(%s,%s%s,%s,%s)",
                                (first_name,last_name,username,email,password,))
            conn.commit()
            print("Registration successful")
        except Exception as e:
            print("Registration failed. Please try again.")
            print(e)
        self.cursor.close()


    def login_user(self):
        self.cursor.execute("SELECT FROM users WHERE username = %s AND password = %s",(username,password,))
        user = self.cursor.fetchone()
        if user:
            print("Login successful")
            return user
        else:
            print("Invalid username or password. Please try again.")
            return None
        self.cursor.close()

    # PLAID

    def create_plaid_details(self):
        try:
            self.cursor.execute("INSERT INTO plaid_client (client_id,client_secret) VALUES(%s,%s)",
                                (client_id,clientsecret,))
            conn.commit()
            print("Plaid registration successful")
        except Exception as e:
            print("Plaid registration failed. Please try again.")
            print(e)
        self.cursor.close()

    def get_plaid_details(self):
        self.cursor.execute("SELECT * FROM plaid_details WHERE user_id = %s",(user_id,))
        plaid_details = self.cursor.fetchone()
        return plaid_details

