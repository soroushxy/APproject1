import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("1vs1 shooter game")
screen.fill('white')
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# Define font
text_font = pygame.font.Font(r'font\Novecentosanswide-DemiBold.otf' , 18)
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

    def collied(self):
        self.score += 10
        self.bullet -= 1

class Bullet:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 5, 5)  # Bullet size
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


Player1 = Player('soroush' ,'red' , 60 , 0 , 10)
Player2 = Player('karen' , 'blue' , 60 , 0 , 10)

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

aim1 = Aim(random.randint(20,1180),random.randint(20,1180) ,  Player1.color)
aim2 = Aim(random.randint(20,1180),random.randint(60,580), Player2.color)
#apples
apple1_surf = pygame.image.load('graphics/apple.png')
apple1_surf = pygame.transform.scale(apple1_surf, (50,50))
apple1_rect = apple1_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
apple2_surf = pygame.image.load('graphics/apple.png')
apple2_surf = pygame.transform.scale(apple2_surf, (50,50))
apple2_rect = apple2_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
apple3_surf = pygame.image.load('graphics/apple.png')
apple3_surf= pygame.transform.scale(apple3_surf, (50,50))
apple3_rect = apple3_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))

#bullet
bullet = pygame.image.load('graphics/bullets.png').convert_alpha()
bullet = pygame.transform.scale(bullet, (50,50))
bullet_rect = bullet.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
bullets = []
#extra time
extra_time = pygame.image.load('graphics/extra-time.png').convert_alpha()
extra_time = pygame.transform.scale(extra_time , (50,50))
etime_rect = extra_time.get_rect(center = (random.randint(20,1180),random.randint(60,580)))
#aim values
aim1_shoot = False
aim2_shoot = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_LEFT:
                aim1.move(-5 , 0)
            if event.key == pygame.K_RIGHT:
                aim1.move(5 , 0)
            if event.key == pygame.K_DOWN:
                aim1.move(0 , 5)
            if event.key == pygame.K_UP:
                aim1.move(0 , -5)
            if event.key == pygame.K_w:
                aim2.move(0,-5)
            if event.key == pygame.K_s:
                aim2.move(0,5)
            if event.key == pygame.K_d:
                aim2.move(5 , 0)
            if event.key == pygame.K_a:
                aim2.move(-5,0)
            if event.key == pygame.K_TAB and Player2.bullet >0:
                aim2_shoot = True
                bullets.append(Bullet(aim2.rect.x , aim2.rect.y , Player2.color))
            if event.key == pygame.K_SPACE and Player1.bullet >0 :
                aim1_shoot = True
                bullets.append(Bullet(aim1.rect.x , aim1.rect.y , Player1.color))
    if apple1_rect.colliderect(aim1.rect) and aim1_shoot == True:
        Player1.collied()
        apple1_rect = apple1_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
    if apple2_rect.colliderect(aim1.rect) and aim1_shoot == True:
        Player1.collied()
        apple2_rect = apple2_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
    if apple3_rect.colliderect(aim1.rect) and aim1_shoot == True:
        Player1.collied()
        apple3_rect = apple3_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
    if apple1_rect.colliderect(aim2.rect) and aim2_shoot == True:
        Player2.collied()
        apple1_rect = apple1_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
    if apple2_rect.colliderect(aim2.rect) and aim2_shoot == True:
        Player2.collied()
        apple2_rect = apple2_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
    if apple3_rect.colliderect(aim2.rect) and aim2_shoot == True:
        Player2.collied()
        apple3_rect = apple3_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
    screen.fill('white')   
    Player1.status(260,25)
    Player2.status(820,25)
    screen.blit(apple1_surf, apple1_rect)
    screen.blit(apple2_surf, apple2_rect)
    screen.blit(apple3_surf, apple3_rect)
    for bullet in bullets:
        bullet.draw(screen)

    # screen.blit(bullet , bullet_rect)
    # screen.blit(extra_time , etime_rect)
    aim1_shoot = False
    aim2_shoot = False
    pygame.display.update()
    clock.tick(60)