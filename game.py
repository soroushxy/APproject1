import pygame
import random
import math

def calculate_extra_points(last_shot_pos, new_shot_pos):
    if last_shot_pos is None: 
        return 0
    distance = math.sqrt((new_shot_pos[0] - last_shot_pos[0])**2 + (new_shot_pos[1] - last_shot_pos[1])**2)
    if distance >=400:
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


pygame.init()

screen = pygame.display.set_mode((840,400))
pygame.display.set_caption("1vs1 shooter game")
screen.fill('white')
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# Define font
text_font = pygame.font.Font(r'font\Novecentosanswide-DemiBold.otf' , 14)
#sound base
shoot_sound = pygame.mixer.Sound('sound/gunshot-hard-sound-fx_B_minor.wav')
reload_sound = pygame.mixer.Sound('sound/gun-reloading-fx.wav')

#player class
class Player:
    def __init__(self,name ,color , time , score , bullet ):
        self.name = name
        self.color = color
        self.time = time
        self.score = score
        self.bullet = bullet
    def status(self  , x,y):
        '''show player info on the screen 
        x,y are the position of topright of the text'''
        txt =text_font.render(f'player:{self.name} , color:{self.color}  , time:{self.time}  , bullets:{self.bullet} , score :{self.score}' , False , 'black')
        txt_rect = txt.get_rect(center=(x,y))
        screen.blit(txt , txt_rect)



class Bullet:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 5, 5)  # Bullet size
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


Player1 = Player('soroush' ,'red' , 60 , 0 , 10)
Player1_last_pos = None
Player2 = Player('karen' , 'blue' , 60 , 0 , 10)
Player2_last_pos = None

# Aim class
class Aim:
    def __init__(self, x, y , color):
        self.x= x
        self.y = y
        self.rect = pygame.Rect(x, y, 5, 5)
        self.color = color  # Create a rectangle for the aim
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

aim1 = Aim(random.randint(20,820),random.randint(20,380) ,  Player1.color)
aim2 = Aim(random.randint(20,820),random.randint(20,380), Player2.color)
#apples
apple1_surf = pygame.image.load('graphics/apple.png')
apple1_surf = pygame.transform.scale(apple1_surf, (50,50))
apple1_rect = apple1_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))
apple2_surf = pygame.image.load('graphics/apple.png')
apple2_surf = pygame.transform.scale(apple2_surf, (50,50))
apple2_rect = apple2_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))
apple3_surf = pygame.image.load('graphics/apple.png')
apple3_surf= pygame.transform.scale(apple3_surf, (50,50))
apple3_rect = apple3_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))

#bullet
class Extra_bullet:
    def __init__(self):
        self.extra_bullet = pygame.image.load('graphics/bullets.png').convert_alpha()
        self.extra_bullet = pygame.transform.scale(self.extra_bullet, (50,50))
        self.extra_bullet_rect = self.extra_bullet.get_rect(center=(random.randint(20,820),random.randint(20,380)))
    def collied(player):
        player.time += 10
extra_bullet1 = Extra_bullet()
extra_bullet1_value = True
extra_bullet1_showvalue = False
extra_bullet2 = Extra_bullet()
extra_bullet2_value = True
extra_bullet2_showvalue = False
bullets = []
#extra time
class Extra_time:
    def __init__(self):
        self.extra_time = pygame.image.load('graphics/extra-time.png').convert_alpha()
        self.extra_time = pygame.transform.scale(self.extra_time, (50,50))
        self.extra_time_rect = self.extra_time.get_rect(center=(random.randint(20,820),random.randint(20,380)))
    
    def collied(player):
        player.time += 10

extra_time1 =  Extra_time()
extra_time1_value = True
extra_time1_showvalue = False
extra_time2 = Extra_time()
extra_time2_value = True
extra_time2_showvalue = False
extra_time3 = Extra_time()
extra_time3_value = True
extra_time3_showvalue = False
extra_time4 = Extra_time()
extra_time4_value = True
extra_time4_showvalue = False

#blind player
class Blind:
    def __init__(self ):
        self.blind = pygame.image.load('graphics/blindfold.png').convert_alpha()
        self.blind = pygame.transform.scale(self.blind , (50,50))
        self.blind_rect = self.blind.get_rect(center=(random.randint(20,820),random.randint(20,380)))
blind1_20 = Blind()
blind1_20_value = True
blind1_60  = Blind()
blind1_60_value = True
blind2_20 = Blind()
blind2_20_value = True
blind2_60 = Blind()
blind2_60_value = True

#aim values
aim1_shoot = False
aim2_shoot = False
#time manager
base_time = pygame.time.get_ticks()
def time_manager():
    global base_time
    current_time = pygame.time.get_ticks()
    delta_time =  (current_time-base_time)//1000
    if delta_time >0 :
        Player1.time -= delta_time
        Player2.time -= delta_time
        base_time = current_time
        if Player1.time < 0:
            Player1.time =0
        if Player2.time <0:
            Player2.time = 0
Player1.bullet = 10000
Player2.bullet = 10000

def end_game():
    if (Player1.time == 0 and Player2.time == 0 ) or (Player1.bullet == 0 and Player2.bullet ==0):
        if Player1.score > Player2.score:
            print(f'{Player1.name} won!')
            exit()
        if Player2.score > Player1.score:
            print(f'{Player2.name} won!')
            exit()
while True:
      
    for i in range(len(bullets)-1,-1,-1):
        if bullets[i].color == Player1.color:
            Player1_last_pos = (bullets[i].x , bullets[i].y) 
            break
    for i in range(len(bullets)-1,-1,-1):
        if bullets[i].color == Player2.color:
            Player2_last_pos = (bullets[i].x , bullets[i].y) 
            break
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            # Player 1 controls
            if event.key == pygame.K_LEFT and aim1.rect.left - 8 > 0:  # Check left edge
                aim1.move(-8, 0)
            if event.key == pygame.K_RIGHT and aim1.rect.right + 8 < 840:  # Check right edge
                aim1.move(8, 0)
            if event.key == pygame.K_DOWN and aim1.rect.bottom + 8 < 400:  # Check bottom edge
                aim1.move(0, 8)
            if event.key == pygame.K_UP and aim1.rect.top - 8 > 20:  # Check top edge
                aim1.move(0, -8)

            # Player 2 controls
            if event.key == pygame.K_w and aim2.rect.top - 8 > 20:  # Check top edge
                aim2.move(0, -8)
            if event.key == pygame.K_s and aim2.rect.bottom + 8 < 400:  # Check bottom edge
                aim2.move(0, 8)
            if event.key == pygame.K_d and aim2.rect.right + 8 < 840:  # Check right edge
                aim2.move(8, 0)
            if event.key == pygame.K_a and aim2.rect.left - 8 > 0:  # Check left edge
                aim2.move(-8, 0)
            if event.key == pygame.K_TAB and Player2.bullet >0 and Player2.time > 0:
                aim2_shoot = True
                Player2.bullet -= 1
                shoot_sound.play()
                bullets.append(Bullet(aim2.rect.x , aim2.rect.y , Player2.color))
            if event.key == pygame.K_SPACE and Player1.bullet >0 and Player1.time >0 :
                aim1_shoot = True
                Player1.bullet -= 1
                shoot_sound.play()
                bullets.append(Bullet(aim1.rect.x , aim1.rect.y , Player1.color))
    
    if apple1_rect.colliderect(aim1.rect) and aim1_shoot == True:
        extra_point = calculate_extra_points(Player1_last_pos , (aim1.rect.x , aim1.rect.y))
        Player1.score += (10+extra_point)
        apple1_rect = apple1_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))
    if apple2_rect.colliderect(aim1.rect) and aim1_shoot == True:
        extra_point = calculate_extra_points(Player1_last_pos , (aim1.rect.x , aim1.rect.y))
        Player1.score += (10+extra_point)
        apple2_rect = apple2_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))
    if apple3_rect.colliderect(aim1.rect) and aim1_shoot == True:
        extra_point = calculate_extra_points(Player1_last_pos , (aim1.rect.x , aim1.rect.y))
        Player1.score += (10+extra_point)
        apple3_rect = apple3_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))
    if apple1_rect.colliderect(aim2.rect) and aim2_shoot == True:
        extra_point = calculate_extra_points(Player2_last_pos , (aim2.rect.x , aim2.rect.y))
        Player2.score += (10+extra_point)
        apple1_rect = apple1_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))
    if apple2_rect.colliderect(aim2.rect) and aim2_shoot == True:
        extra_point = calculate_extra_points(Player2_last_pos , (aim2.rect.x , aim2.rect.y))
        Player2.score += (10+extra_point)
        apple2_rect = apple2_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))
    if apple3_rect.colliderect(aim2.rect) and aim2_shoot == True:
        extra_point = calculate_extra_points(Player2_last_pos , (aim2.rect.x , aim2.rect.y))
        Player2.score += (10+extra_point)
        apple3_rect = apple3_surf.get_rect(center=(random.randint(20,820),random.randint(20,380)))
    counter1 = 1
    if Player1.time < 40 and counter1 >0 :
        extra_time1_showvalue =True
        counter1-= 1
    counter2 = 1
    if Player2.time < 40 and counter2 >0 :
        extra_time2_showvalue = True
        counter2 -= 1
    counter3 = 1
    if Player1.time <20 and counter3 >0:
        extra_time3_showvalue = True
        counter3 -=1
    counter4 = 1
    if Player2.time < 20 and counter4 > 0:
        extra_time4_showvalue = True
        counter4 -= 1
    if extra_time1.extra_time_rect.colliderect(aim1.rect) and aim1_shoot and extra_time1_value and extra_time1_showvalue :
        Player1.time += 10
        extra_time1_value = False
        extra_time1_showvalue = False

    if extra_time1.extra_time_rect.colliderect(aim2.rect) and aim2_shoot and extra_time1_value and extra_time1_showvalue :
        Player2.time += 10
        extra_time1_value = False
        extra_time1_showvalue = False

    if extra_time2.extra_time_rect.colliderect(aim1.rect) and aim1_shoot and extra_time2_value and extra_time2_showvalue :
        Player1.time += 10
        extra_time2_value = False
        extra_time2_showvalue = False
    if extra_time2.extra_time_rect.colliderect(aim2.rect) and aim2_shoot and extra_time2_value and extra_time2_showvalue :
        Player2.time += 10
        extra_time2_value = False
        extra_time2_showvalue = False
    if extra_time3.extra_time_rect.colliderect(aim1.rect) and aim1_shoot and extra_time3_value and extra_time3_showvalue :
        Player1.time += 10
        extra_time3_value = False
        extra_time3_showvalue = False
    if extra_time3.extra_time_rect.colliderect(aim2.rect) and aim2_shoot and extra_time3_value and extra_time3_showvalue :
        Player2.time += 10
        extra_time3_value = False
        extra_time3_showvalue = False
    if extra_time4.extra_time_rect.colliderect(aim1.rect) and aim1_shoot and extra_time4_value and extra_time4_showvalue :
        Player1.time += 10
        extra_time4_value = False
        extra_time4_showvalue = False
    if extra_time4.extra_time_rect.colliderect(aim2.rect) and aim2_shoot and extra_time4_value and extra_time4_showvalue :
        Player2.time += 10
        extra_time4_value = False
        extra_time4_showvalue = False

    counter5 = 1
    if Player1.bullet <= 5 and counter5 > 0 :
        extra_bullet1_showvalue = True
        counter5 -= 1
    counter6 = 1
    if Player2.bullet <= 5 and counter6 >0 :
        extra_bullet2_showvalue = True
        counter6 -= 1
    if extra_bullet1.extra_bullet_rect.colliderect(aim1.rect) and aim1_shoot and extra_bullet1_value and extra_bullet1_showvalue:
        Player1.bullet += 5
        extra_bullet1_value = False  
        extra_bullet1_showvalue = False  
        reload_sound.play()
    if extra_bullet1.extra_bullet_rect.colliderect(aim2.rect) and aim2_shoot and extra_bullet1_value and extra_bullet1_showvalue:
        Player2.bullet += 5
        extra_bullet1_value =False
        extra_bullet1_showvalue = False
        reload_sound.play()
    if extra_bullet2.extra_bullet_rect.colliderect(aim1.rect) and aim1_shoot and extra_bullet2_value and extra_bullet2_showvalue:
        Player1.bullet += 5
        extra_bullet2_value = False
        extra_bullet2_showvalue = False
        reload_sound.play()
    if extra_bullet2.extra_bullet_rect.colliderect(aim2.rect) and aim2_shoot and extra_bullet2_value and extra_bullet2_showvalue:
        Player2.bullet += 5
        extra_bullet2_value = False
        extra_bullet2_showvalue = False
        reload_sound.play()
    if blind1_20.blind_rect.colliderect(aim1.rect) and aim1_shoot and blind1_20_value and Player1.score >= 20:
        aim2 = Aim(random.randint(20,820),random.randint(20,380), Player2.color)
        blind1_20_value = False
    if blind1_20.blind_rect.colliderect(aim2.rect) and aim2_shoot and blind1_20_value and Player1.score >= 20:
        aim1 = Aim(random.randint(20,820),random.randint(20,380) , Player1.color)   
        blind1_20_value = False
    if blind2_20.blind_rect.colliderect(aim1.rect) and aim1_shoot and blind2_20_value and Player2.score >= 20:
        aim2 = Aim(random.randint(20,820),random.randint(20,380), Player2.color)
        blind2_20_value = False
    if blind2_20.blind_rect.colliderect(aim2.rect) and aim2_shoot and blind2_20_value and Player2.score >= 20:
        aim1 = Aim(random.randint(20,820),random.randint(20,380), Player1.color)
        blind2_20_value = False
    if blind1_60.blind_rect.colliderect(aim1.rect) and aim1_shoot and blind1_60_value and Player1.score >= 60:
        aim2 = Aim(random.randint(20,820),random.randint(20,380), Player2.color)
        blind1_60_value = False
    if blind1_60.blind_rect.colliderect(aim2.rect) and aim2_shoot and blind1_60_value and Player1.score >= 60:
        aim1 = Aim(random.randint(20,820),random.randint(20,380) , Player1.color)
        blind1_60_value = False
    if blind2_60.blind_rect.colliderect(aim1.rect) and aim1_shoot and blind2_60_value and Player2.score >= 60:
        aim2 = Aim(random.randint(20,820),random.randint(20,380), Player2.color)
        blind2_60_value = False
    if blind2_60.blind_rect.colliderect(aim2.rect) and aim2_shoot and blind2_60_value and Player2.score >= 60:
        aim1 = Aim(random.randint(20,820),random.randint(20,380), Player1.color)
        blind2_60_value = False
    screen.fill('white')   
    if extra_time1_showvalue and extra_time1_value :
        screen.blit(extra_time1.extra_time , extra_time1.extra_time_rect)
    if extra_time2_showvalue and extra_time2_value:
        screen.blit(extra_time2.extra_time , extra_time2.extra_time_rect)
    if extra_time3_showvalue and extra_time3_value:
        screen.blit(extra_time3.extra_time , extra_time3.extra_time_rect)
    if extra_time4_showvalue and extra_time4_value:
        screen.blit(extra_time4.extra_time , extra_time4.extra_time_rect)
    if extra_bullet1_showvalue and extra_bullet1_value:
        screen.blit(extra_bullet1.extra_bullet , extra_bullet1.extra_bullet_rect)
    if extra_bullet2_showvalue and extra_bullet2_value:
        screen.blit(extra_bullet2.extra_bullet , extra_bullet2.extra_bullet_rect)
    if Player1.score >= 20 and blind1_20_value:
        screen.blit(blind1_20.blind , blind1_20.blind_rect)
    if Player2.score >= 20 and blind2_20_value:
        screen.blit(blind2_20.blind , blind2_20.blind_rect)
    if Player2.score >= 20 and blind2_20_value:
        screen.blit(blind2_20.blind , blind2_20.blind_rect)
    if Player1.score >= 60 and blind1_60_value:
        screen.blit(blind1_60.blind , blind1_60.blind_rect)
    if Player2.score >= 60 and blind2_60_value:
        screen.blit(blind2_60.blind , blind2_60.blind_rect)
    Player1.status(210,10)
    Player2.status(210,20)
    screen.blit(apple1_surf, apple1_rect)
    screen.blit(apple2_surf, apple2_rect)
    screen.blit(apple3_surf, apple3_rect)
    for bullet in bullets:
        bullet.draw(screen)

    aim1_shoot = False
    aim2_shoot = False
    time_manager()
    # end_game()
    pygame.display.update()
    clock.tick(60)