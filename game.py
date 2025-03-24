import pygame
import random
import math
import login  # Direct import for login system
import sys


def calculate_extra_points(last_shot_pos, new_shot_pos):
    if last_shot_pos is None: 
        return 0
    distance = math.sqrt((new_shot_pos[0] - last_shot_pos[0])**2 + (new_shot_pos[1] - last_shot_pos[1])**2)
    if distance >= 400:
        return 5
    elif distance >= 300:
        return 4
    elif distance >= 200:
        return 3
    elif distance >= 100:
        return 2
    elif distance >= 50:
        return 1
    else:
        return 0

def run_game(player1_name, player2_name):
    pygame.init()
    screen = pygame.display.set_mode((840, 400))
    pygame.display.set_caption("1vs1 shooter game")
    screen.fill('white')
    clock = pygame.time.Clock()

    # Define colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    # Define font
    text_font = pygame.font.Font(r'font\Novecentosanswide-DemiBold.otf', 14)
    # Sound base
    shoot_sound = pygame.mixer.Sound('sound/gunshot-hard-sound-fx_B_minor.wav')
    reload_sound = pygame.mixer.Sound('sound/gun-reloading-fx.wav')

    # Player class
    class Player:
        def __init__(self, name, color, time, score, bullet):
            self.name = name
            self.color = color
            self.time = time
            self.score = score
            self.bullet = bullet
            self.last_shot_hit_apple = False 
        def status(self, x, y):
            txt = text_font.render(f'player:{self.name} , color:{self.color}  , time:{self.time}  , bullets:{self.bullet} , score :{self.score}', False, 'black')
            txt_rect = txt.get_rect(center=(x, y))
            screen.blit(txt, txt_rect)

    class Bullet:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, 5, 5)
            self.color = color
        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)

    class Target:
        def __init__(self, image_path, size=(50, 50)):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
            self.rect = self.image.get_rect(center=(random.randint(20, 820), random.randint(20, 380)))

    class Apple(Target):
        def __init__(self):
            super().__init__('graphics/apple.png')

    class Extra_bullet(Target):
        def __init__(self):
            super().__init__('graphics/bullets.png')
        def collied(self, player):  # Assuming this was your original spelling
            player.bullet += 5

    class Extra_time(Target):
        def __init__(self):
            super().__init__('graphics/extra-time.png')
        def collied(self, player):  # Assuming this was your original spelling
            player.time += 10

    class Blind(Target):
        def __init__(self):
            super().__init__('graphics/blindfold.png')

    class Aim:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, 5, 5)
            self.color = color
        def move(self, dx, dy):
            self.rect.x += dx
            self.rect.y += dy

    # Initialize game objects with dynamic player names
    Player1 = Player(player1_name, 'red', 60, 0, 10)
    Player1_last_pos = None
    Player2 = Player(player2_name, 'blue', 60, 0, 10)
    Player2_last_pos = None
    aim1 = Aim(random.randint(20, 820), random.randint(20, 380), Player1.color)
    aim2 = Aim(random.randint(20, 820), random.randint(20, 380), Player2.color)
    apple1 = Apple()
    apple2 = Apple()
    apple3 = Apple()
    extra_bullet1 = Extra_bullet()
    extra_bullet2 = Extra_bullet()
    extra_time1 = Extra_time()
    extra_time2 = Extra_time()
    extra_time3 = Extra_time()
    extra_time4 = Extra_time()
    blind1_20 = Blind()
    blind1_60 = Blind()
    blind2_20 = Blind()
    blind2_60 = Blind()

    # Initialize flags and counters outside loop
    bullets = []
    aim1_shoot = False
    aim2_shoot = False
    extra_bullet1_value = True
    extra_bullet1_showvalue = False
    extra_bullet2_value = True
    extra_bullet2_showvalue = False
    extra_time1_value = True
    extra_time1_showvalue = False
    extra_time2_value = True
    extra_time2_showvalue = False
    extra_time3_value = True
    extra_time3_showvalue = False
    extra_time4_value = True
    extra_time4_showvalue = False
    blind1_20_value = True
    blind1_60_value = True
    blind2_20_value = True
    blind2_60_value = True
    counter1 = 1
    counter2 = 1
    counter3 = 1
    counter4 = 1
    counter5 = 1
    counter6 = 1

    base_time = pygame.time.get_ticks()

    def time_manager():
        nonlocal base_time
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - base_time) // 1000
        if delta_time > 0:
            Player1.time -= delta_time
            Player2.time -= delta_time
            base_time = current_time
            if Player1.time < 0:
                Player1.time = 0
            if Player2.time < 0:
                Player2.time = 0

    def end_game():
        if (Player1.time == 0 or Player1.bullet == 0) and (Player2.bullet == 0 or Player2.time == 0):
            return True
        return False

    # Main game loop
    running = True
    while running:
        for i in range(len(bullets)-1, -1, -1):
            if bullets[i].color == Player1.color:
                Player1_last_pos = (bullets[i].x, bullets[i].y)
                break
        for i in range(len(bullets)-1, -1, -1):
            if bullets[i].color == Player2.color:
                Player2_last_pos = (bullets[i].x, bullets[i].y)
                break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and aim1.rect.left - 8 > 0:
                    aim1.move(-8, 0)
                if event.key == pygame.K_RIGHT and aim1.rect.right + 8 < 840:
                    aim1.move(8, 0)
                if event.key == pygame.K_DOWN and aim1.rect.bottom + 8 < 400:
                    aim1.move(0, 8)
                if event.key == pygame.K_UP and aim1.rect.top - 8 > 20:
                    aim1.move(0, -8)
                if event.key == pygame.K_w and aim2.rect.top - 8 > 20:
                    aim2.move(0, -8)
                if event.key == pygame.K_s and aim2.rect.bottom + 8 < 400:
                    aim2.move(0, 8)
                if event.key == pygame.K_d and aim2.rect.right + 8 < 840:
                    aim2.move(8, 0)
                if event.key == pygame.K_a and aim2.rect.left - 8 > 0:
                    aim2.move(-8, 0)
                if event.key == pygame.K_TAB and Player2.bullet > 0 and Player2.time > 0:
                    aim2_shoot = True
                    Player2.bullet -= 1
                    shoot_sound.play()
                    bullets.append(Bullet(aim2.rect.x, aim2.rect.y, Player2.color))
                if event.key == pygame.K_SPACE and Player1.bullet > 0 and Player1.time > 0:
                    aim1_shoot = True
                    Player1.bullet -= 1
                    shoot_sound.play()
                    bullets.append(Bullet(aim1.rect.x, aim1.rect.y, Player1.color))
        hit_apple1 = False
        hit_apple2 = False
        # Collision detection
        for apple in [apple1, apple2, apple3]:
            if apple.rect.colliderect(aim1.rect) and aim1_shoot:
                extra_point = calculate_extra_points(Player1_last_pos, (aim1.rect.x, aim1.rect.y))
                Player1.score += (10 + extra_point)
                if Player1.last_shot_hit_apple:
                    Player1.score += 2
                Player1.last_shot_hit_apple = True
                hit_apple1 = True
                apple.rect.center = (random.randint(20, 820), random.randint(20, 380))
            if apple.rect.colliderect(aim2.rect) and aim2_shoot:
                extra_point = calculate_extra_points(Player2_last_pos, (aim2.rect.x, aim2.rect.y))
                Player2.score += (10 + extra_point)
                if Player2.last_shot_hit_apple:
                    Player2.score += 2
                Player2.last_shot_hit_apple = True
                hit_apple2 = True
                apple.rect.center = (random.randint(20, 820), random.randint(20, 380))
        if aim1_shoot and not hit_apple1:
            Player1.last_shot_hit_apple = False
        if aim2_shoot and not hit_apple2:
            Player2.last_shot_hit_apple = False
        # Extra time spawning logic
        if Player1.time < 40 and counter1 > 0:
            extra_time1_showvalue = True
            counter1 -= 1
        if Player2.time < 40 and counter2 > 0:
            extra_time2_showvalue = True
            counter2 -= 1
        if Player1.time < 20 and counter3 > 0:
            extra_time3_showvalue = True
            counter3 -= 1
        if Player2.time < 20 and counter4 > 0:
            extra_time4_showvalue = True
            counter4 -= 1

        # Extra time collision (simple, working logic)
        if extra_time1_showvalue and extra_time1_value and extra_time1.rect.colliderect(aim1.rect) and aim1_shoot:
            extra_time1.collied(Player1)
            extra_time1_value = False
            extra_time1_showvalue = False
        if extra_time1_showvalue and extra_time1_value and extra_time1.rect.colliderect(aim2.rect) and aim2_shoot:
            extra_time1.collied(Player2)
            extra_time1_value = False
            extra_time1_showvalue = False
        if extra_time2_showvalue and extra_time2_value and extra_time2.rect.colliderect(aim1.rect) and aim1_shoot:
            extra_time2.collied(Player1)
            extra_time2_value = False
            extra_time2_showvalue = False
        if extra_time2_showvalue and extra_time2_value and extra_time2.rect.colliderect(aim2.rect) and aim2_shoot:
            extra_time2.collied(Player2)
            extra_time2_value = False
            extra_time2_showvalue = False
        if extra_time3_showvalue and extra_time3_value and extra_time3.rect.colliderect(aim1.rect) and aim1_shoot:
            extra_time3.collied(Player1)
            extra_time3_value = False
            extra_time3_showvalue = False
        if extra_time3_showvalue and extra_time3_value and extra_time3.rect.colliderect(aim2.rect) and aim2_shoot:
            extra_time3.collied(Player2)
            extra_time3_value = False
            extra_time3_showvalue = False
        if extra_time4_showvalue and extra_time4_value and extra_time4.rect.colliderect(aim1.rect) and aim1_shoot:
            extra_time4.collied(Player1)
            extra_time4_value = False
            extra_time4_showvalue = False
        if extra_time4_showvalue and extra_time4_value and extra_time4.rect.colliderect(aim2.rect) and aim2_shoot:
            extra_time4.collied(Player2)
            extra_time4_value = False
            extra_time4_showvalue = False

        # Extra bullet spawning logic
        if Player1.bullet <= 5 and counter5 > 0:
            extra_bullet1_showvalue = True
            counter5 -= 1
        if Player2.bullet <= 5 and counter6 > 0:
            extra_bullet2_showvalue = True
            counter6 -= 1

        # Extra bullet collision (simple, working logic with reload sound)
        if extra_bullet1_showvalue and extra_bullet1_value and extra_bullet1.rect.colliderect(aim1.rect) and aim1_shoot:
            extra_bullet1.collied(Player1)
            extra_bullet1_value = False
            extra_bullet1_showvalue = False
            reload_sound.play()
        if extra_bullet1_showvalue and extra_bullet1_value and extra_bullet1.rect.colliderect(aim2.rect) and aim2_shoot:
            extra_bullet1.collied(Player2)
            extra_bullet1_value = False
            extra_bullet1_showvalue = False
            reload_sound.play()
        if extra_bullet2_showvalue and extra_bullet2_value and extra_bullet2.rect.colliderect(aim1.rect) and aim1_shoot:
            extra_bullet2.collied(Player1)
            extra_bullet2_value = False
            extra_bullet2_showvalue = False
            reload_sound.play()
        if extra_bullet2_showvalue and extra_bullet2_value and extra_bullet2.rect.colliderect(aim2.rect) and aim2_shoot:
            extra_bullet2.collied(Player2)
            extra_bullet2_value = False
            extra_bullet2_showvalue = False
            reload_sound.play()

        # Blind collision
        if blind1_20_value and Player1.score >= 20 and blind1_20.rect.colliderect(aim1.rect) and aim1_shoot:
            aim2 = Aim(random.randint(20, 820), random.randint(20, 380), Player2.color)
            blind1_20_value = False
        if blind1_20_value and Player1.score >= 20 and blind1_20.rect.colliderect(aim2.rect) and aim2_shoot:
            aim1 = Aim(random.randint(20, 820), random.randint(20, 380), Player1.color)
            blind1_20_value = False
        if blind1_60_value and Player1.score >= 60 and blind1_60.rect.colliderect(aim1.rect) and aim1_shoot:
            aim2 = Aim(random.randint(20, 820), random.randint(20, 380), Player2.color)
            blind1_60_value = False
        if blind1_60_value and Player1.score >= 60 and blind1_60.rect.colliderect(aim2.rect) and aim2_shoot:
            aim1 = Aim(random.randint(20, 820), random.randint(20, 380), Player1.color)
            blind1_60_value = False
        if blind2_20_value and Player2.score >= 20 and blind2_20.rect.colliderect(aim1.rect) and aim1_shoot:
            aim2 = Aim(random.randint(20, 820), random.randint(20, 380), Player2.color)
            blind2_20_value = False
        if blind2_20_value and Player2.score >= 20 and blind2_20.rect.colliderect(aim2.rect) and aim2_shoot:
            aim1 = Aim(random.randint(20, 820), random.randint(20, 380), Player1.color)
            blind2_20_value = False
        if blind2_60_value and Player2.score >= 60 and blind2_60.rect.colliderect(aim1.rect) and aim1_shoot:
            aim2 = Aim(random.randint(20, 820), random.randint(20, 380), Player2.color)
            blind2_60_value = False
        if blind2_60_value and Player2.score >= 60 and blind2_60.rect.colliderect(aim2.rect) and aim2_shoot:
            aim1 = Aim(random.randint(20, 820), random.randint(20, 380), Player1.color)
            blind2_60_value = False

        # Drawing
        screen.fill('white')
        if extra_time1_showvalue and extra_time1_value:
            screen.blit(extra_time1.image, extra_time1.rect)
        if extra_time2_showvalue and extra_time2_value:
            screen.blit(extra_time2.image, extra_time2.rect)
        if extra_time3_showvalue and extra_time3_value:
            screen.blit(extra_time3.image, extra_time3.rect)
        if extra_time4_showvalue and extra_time4_value:
            screen.blit(extra_time4.image, extra_time4.rect)
        if extra_bullet1_showvalue and extra_bullet1_value:
            screen.blit(extra_bullet1.image, extra_bullet1.rect)
        if extra_bullet2_showvalue and extra_bullet2_value:
            screen.blit(extra_bullet2.image, extra_bullet2.rect)
        if Player1.score >= 20 and blind1_20_value:
            screen.blit(blind1_20.image, blind1_20.rect)
        if Player2.score >= 20 and blind2_20_value:
            screen.blit(blind2_20.image, blind2_20.rect)
        if Player1.score >= 60 and blind1_60_value:
            screen.blit(blind1_60.image, blind1_60.rect)
        if Player2.score >= 60 and blind2_60_value:
            screen.blit(blind2_60.image, blind2_60.rect)
        Player1.status(210, 10)
        Player2.status(210, 20)
        screen.blit(apple1.image, apple1.rect)
        screen.blit(apple2.image, apple2.rect)
        screen.blit(apple3.image, apple3.rect)
        for bullet in bullets:
            bullet.draw(screen)

        aim1_shoot = False
        aim2_shoot = False
        time_manager()
        if end_game():
            running = False

        pygame.display.update()
        clock.tick(60)
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
                pygame.quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    end = False
                    pygame.quit
                    sys.exit()
                elif event.key == pygame.K_r:
                    end = False
                    run_game(Player1.name , Player2.name)
                elif event.key == pygame.K_l:
                    end= False
                    main()
        screen.fill('white')
        if Player1.score > Player2.score:
            winner_text = text_font.render(f'{Player1.name} WON! \n {Player1.name} score : {Player1.score} \n {Player2.name} score : {Player2.score}'  , False , 'black')
            winner_text_rect = winner_text.get_rect(center=(420, 100))
            screen.blit(winner_text, winner_text_rect)
        elif Player1.score < Player2.score:
            winner_text = text_font.render(f'{Player2.name} WON! \n {Player2.name} score : {Player2.score} \n {Player1.name} score : {Player1.score}'  , False , 'black')
            winner_text_rect = winner_text.get_rect(center=(420, 100))
            screen.blit(winner_text, winner_text_rect)
        else:
            winner_text = text_font.render(f'DRAW! \n {Player1.name} score : {Player1.score} \n {Player2.name} score : {Player2.score}'  , False , 'black')
            winner_text_rect = winner_text.get_rect(center=(420, 100))
            screen.blit(winner_text, winner_text_rect)
        end_txt = text_font.render('Press E to exit press R to restart the game press L to go back to the login page', False, 'black')
        end_txt_rect = end_txt.get_rect(center=(420, 300))
        screen.blit(end_txt , end_txt_rect)
        pygame.display.update()

# Main execution
def main():
    # Login for Player 1
    app1 = login.LoginSignupApp(1)  # Use explicit module reference
    success1, player1_name = app1.run()
    if not success1:
        pygame.quit()
        sys.exit()

    # Login for Player 2
    app2 = login.LoginSignupApp(2)  # Use explicit module reference
    success2, player2_name = app2.run()
    if not success2:
        pygame.quit()
        sys.exit()

    # Run game with both player names if both logins succeed
    if success1 and success2:
        run_game(player1_name, player2_name)
    else:
        pygame.quit()
main()