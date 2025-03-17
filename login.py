import sqlite3

# creating database : 
def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL)''')
    conn.commit()
    conn.close()


# create class for login and signup :
class UserManager:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name

    def signup(self, username, password, email):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                           (username, password, email))
            conn.commit()
            return True, "Signup successful!"
        except sqlite3.IntegrityError:
            return False, "Username or email\n  already exists!"
        finally:
            conn.close()

    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return True, "Login successful!"
        return False, "Invalid username \n or password!"
