import sqlite3
import pygame
import pygame_gui
import re
import bcrypt  


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

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

def is_valid_username(username):
    return len(username) >= 5

def is_valid_password(password):
    return len(password) >= 8

class UserManager:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name

    def signup(self, username, password, email):
        if not is_valid_username(username):
            return False, "Username must be at\n least 5 characters!"
        if not is_valid_password(password):
            return False, "Password must be at\n least 8 characters!"
        if not is_valid_email(email):
            return False, "Invalid email address!"

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                           (username, hashed_password, email))
            conn.commit()
            return True, "Signup successful!"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists!"
        finally:
            conn.close()

    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            # Retrieve the stored hashed password (as bytes)
            stored_hashed_password = user[0]
            # Check if the provided password matches the stored hash
            if isinstance(stored_hashed_password, str):  # Handle case where password might be stored as string
                stored_hashed_password = stored_hashed_password.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                return True, "Login successful!"
        return False, "Invalid username \n or password!"

class LoginSignupApp:
    def __init__(self, player_number):  
        print(f"Initializing LoginSignupApp for Player {player_number}")
        pygame.init()
        self.WIDTH, self.HEIGHT = 400, 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(f"Login / Signup - Player {player_number}")
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.user_manager = UserManager()
        self.background_image = pygame.image.load("login graphics/photo_2025-03-22_19-49-35.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        self.player_number = player_number
        self.create_signup_ui()
        self.logged_in = False
        self.username = None

    def create_signup_ui(self):
        self.clear_ui()
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 100), (200, 30)), placeholder_text="username", manager=self.manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 150), (200, 30)), placeholder_text="password", manager=self.manager)
        self.email_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 200), (200, 30)), placeholder_text="email", manager=self.manager)
        self.signup_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 250), (200, 40)), text="Sign Up", manager=self.manager)
        self.switch_to_login_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 300), (200, 40)), text="Go to Login", manager=self.manager)

    def create_login_ui(self):
        self.clear_ui()
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 100), (200, 30)), placeholder_text="username", manager=self.manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 150), (200, 30)), placeholder_text="password", manager=self.manager)
        self.login_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 200), (200, 40)), text="Login", manager=self.manager)
        self.switch_to_signup_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 250), (200, 40)), text="Go to Signup", manager=self.manager)

    def clear_ui(self):
        self.manager.clear_and_reset()

    def run(self):
        running = True
        self.error_message = ""
        error_timer = 0
        
        while running and not self.logged_in:
            time_delta = self.clock.tick(30) / 1000.0
            self.screen.blit(self.background_image, (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.signup_button:
                        username = self.username_entry.get_text().strip()
                        password = self.password_entry.get_text().strip()
                        email = self.email_entry.get_text().strip()
                        if not username or not password or not email:
                            self.error_message = "All fields are required!"
                            error_timer = pygame.time.get_ticks()
                        else:
                            success, msg = self.user_manager.signup(username, password, email)
                            self.error_message = msg
                            error_timer = pygame.time.get_ticks()
                            if success:
                                self.create_login_ui()
                    elif event.ui_element == self.switch_to_login_button:
                        self.create_login_ui()
                    elif event.ui_element == self.login_button:
                        username = self.username_entry.get_text().strip()
                        password = self.password_entry.get_text().strip()
                        if not username or not password:
                            self.error_message = "Username and password\n          are required!"
                            error_timer = pygame.time.get_ticks()
                        else:
                            success, msg = self.user_manager.login(username, password)
                            self.error_message = msg
                            error_timer = pygame.time.get_ticks()
                            if success:
                                self.logged_in = True
                                self.username = username
                    elif event.ui_element == self.switch_to_signup_button:
                        self.create_signup_ui()
                self.manager.process_events(event)
            
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            
            if self.error_message:
                font = pygame.font.Font(None, 24)
                text_surface = font.render(self.error_message, True, (255, 250, 250))
                self.screen.blit(text_surface, (120, self.HEIGHT - 100))
                if pygame.time.get_ticks() - error_timer > 2000:
                    self.error_message = ""

            pygame.display.update()
        
        if not self.logged_in:
            pygame.quit()
        return self.logged_in, self.username


create_database()

if __name__ == "__main__":
    app = LoginSignupApp(1)
    success, username = app.run()
    if success:
        print(f"Logged in as {username}")