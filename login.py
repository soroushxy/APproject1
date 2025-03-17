import sqlite3
import pygame
import pygame_gui

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
    
class LoginSignupApp:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 400, 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Login / Signup")
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.user_manager = UserManager()
        self.create_signup_ui()

    def create_signup_ui(self):
        self.clear_ui()
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 100), (200, 30)),placeholder_text="username",manager =self.manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 150), (200, 30)),placeholder_text="password", manager=self.manager)
        self.email_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 200), (200, 30)),placeholder_text="email" ,manager=self.manager)
        self.signup_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 250), (200, 40)), text="Sign Up", manager=self.manager)
        self.switch_to_login_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 300), (200, 40)), text="Go to Login", manager=self.manager)

    def create_login_ui(self):
        self.clear_ui()
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 100), (200, 30)),placeholder_text="username", manager=self.manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 150), (200, 30)),placeholder_text="password", manager=self.manager)
        self.login_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 200), (200, 40)), text="Login", manager=self.manager)
        self.switch_to_signup_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 250), (200, 40)), text="Go to Signup", manager=self.manager)

    def clear_ui(self):
        self.manager.clear_and_reset()

    def show_message(self, message):
        font = pygame.font.Font(None, 25)
        text_surface = font.render(message, True, (250, 250,250))
        self.screen.blit(text_surface, (130, 200))
        pygame.display.update()
        pygame.time.delay(3000)
