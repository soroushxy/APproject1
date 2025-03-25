import sqlite3
import pygame
import sys 

# create the database for scores
def init_leaderboard_db():
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call this once at the start of the program
init_leaderboard_db()

# Save a player score to the leaderboard
def save_score(player_name, score):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO leaderboard (player_name, score) VALUES (?, ?)', (player_name, score))
    conn.commit()
    conn.close()

# Get the top scores
def get_top_scores(limit=5):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute('SELECT player_name, score FROM leaderboard ORDER BY score DESC LIMIT ?', (limit,))
    top_scores = cursor.fetchall()
    conn.close()
    return top_scores

# Display leaderboard function
def display_leaderboard(screen):
    top_scores = get_top_scores(5)  # Get top 5 scores
    leaderboard_font = pygame.font.Font(r'font\Novecentosanswide-DemiBold.otf', 20)
    screen.fill('white')

    # Background image
    end_image = pygame.image.load('graphics/end.jpg')
    end_image_rect = end_image.get_rect(center=(420, 200))
    screen.blit(end_image, end_image_rect)

    
    title = leaderboard_font.render("Leaderboard", True, 'black')
    title_rect = title.get_rect(center=(420, 50))
    screen.blit(title, title_rect)

    # Display top scores
    y = 100
    for i, (player_name, score) in enumerate(top_scores, 1):
        entry = leaderboard_font.render(f"{i}. {player_name}: {score}", True, 'white')
        entry_rect = entry.get_rect(center=(420, y))
        screen.blit(entry, entry_rect)
        y += 40

    # Instructions
    instructions = leaderboard_font.render("Press B to go back", True, 'red')
    instructions_rect = instructions.get_rect(center=(420, 350))
    screen.blit(instructions, instructions_rect)

    pygame.display.update()

#   Going back
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  
                    waiting = False