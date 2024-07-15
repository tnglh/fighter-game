import pygame
from fighter import Fighter
pygame.init()

SCREEN_WEIGHT = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WEIGHT,SCREEN_HEIGHT))
pygame.display.set_caption("FIGHTER")
clock = pygame.time.Clock()

game_active = True

#set background
background = pygame.image.load("/Users/Toan/PycharmProjects/fighter-game/graphics/background.jpg").convert()
scale_bg = pygame.transform.scale(background,(SCREEN_WEIGHT,SCREEN_HEIGHT))

victory = pygame.image.load("/Users/Toan/PycharmProjects/fighter-game/graphics/victory.png").convert()

def draw_bg():
    screen.blit(scale_bg, (0, 0))
def draw_vic():
    screen.blit(victory,(360,150))
# draw hp bar
def draw_hpbar(health,x,y):
    ratio = health/100
    pygame.draw.rect(screen,(255,255,255),(x-2,y-2,404,34))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 400, 30))
    pygame.draw.rect(screen, (0,255,0),(x,y,400*ratio,30))
#load character sheet
warrior_sheet = pygame.image.load("graphics/Fantasy Warrior copy/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("graphics/EVil Wizard 2 copy/Sprites/wizard.png").convert_alpha()
#set data for character
WARRIOR_SIZE =162
WARRIOR_SCALE = 4
WARRIOR_OFFSET =[72,56]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]

WIZARD_SIZE=250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

#load character animation step
WARRIOR_ANIMATION_STEPS= [10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS = [8,8,1,8,8,3,7]

#set character
fighter1 = Fighter(1,200,310,screen,False,warrior_sheet,WARRIOR_ANIMATION_STEPS,WARRIOR_DATA)
fighter2 = Fighter(2,500,310,screen,True,wizard_sheet,WIZARD_ANIMATION_STEPS,WIZARD_DATA)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         fighter1.jump()

    if game_active == True:
        draw_bg()
        draw_hpbar(fighter1.health,20,20)
        draw_hpbar(fighter2.health,580,20)
        fighter1.draw()
        fighter1.update(fighter2)

        fighter2.draw()
        fighter2.update(fighter1)
        if fighter1.death == True or fighter2.death == True:
            game_active = False
    else:
        draw_vic()

    pygame.display.update()
    clock.tick(60)