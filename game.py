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
class Player:
    def __init__(self,name ,color , time , score , bullet  ):
        self.name = name
        self.color = color
        self.time = time
        self.score = score
        self.bullet = bullet
    def draw(self  , x,y):
        '''show player info on the screen 
        x,y are the position of topright of the text'''
        txt =text_font.render(f'player:{self.name} , color:{self.color}  , time:{self.time}  , bullets:{self.bullet} , score :{self.score}' , False , 'black')
        txt_rect = txt.get_rect(center=(x,y))
        screen.blit(txt , txt_rect)
        

Player1 = Player('soroush' ,'red' , 60 , 0 , 10)
Player2 = Player('karen' , 'blue' , 60 , 0 , 10)

# Aim class
class Aim:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 5)  # Create a rectangle for the aim

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)  # Draw the aim as a red rectangle

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
aim = Aim(390, 290)  # Position the aim in the center of the screen

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

e = pygame.USEREVENT + 1
pygame.time.set_timer(e , 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == e:
            screen.fill('white')
            apple1_rect = apple1_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
            apple2_rect = apple2_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
            apple3_rect = apple3_surf.get_rect(center=(random.randint(20,1180),random.randint(60,580)))
        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_LEFT:
                aim.move(-5 , 0)
            if event.key == pygame.K_RIGHT:
                aim.move(5 , 0)
            if event.key == pygame.K_DOWN:
                aim.move(0 , 5)
            if event.key == pygame.K_UP:
                aim.move(0 , -5)
    Player1.draw(260,25)
    Player2.draw(820,25)
    screen.blit(apple1_surf, apple1_rect)
    screen.blit(apple2_surf, apple2_rect)
    screen.blit(apple3_surf, apple3_rect)
    aim.draw(screen)
    screen.blit(bullet , bullet_rect)

    pygame.display.update()
    clock.tick(20)
