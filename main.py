import pygame
from player import Player

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prism Girlz")

#frame rate
clock = pygame.time.Clock()
FPS = 60

# player variables for spritesheet
#player_one_size =

# bg image
bg_image = pygame.image.load("backgroundimage.jpeg")

# load sprite sheets
spritesheetdemo_img = pygame.image.load("assets/images/spritesheetdemo/spritesheetdemo.png").convert_alpha()

# animation
player_one_steps = [5, 9, 5, 5, 1]

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

def health_bar(health, x, y):
    update_health = health / 100
    pygame.draw.rect(screen, (0, 0, 0), (x-1, y-1, 403, 33))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 400, 30))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 400 * update_health, 30))

# create two instances of the players
player_1 = Player(200, 310, spritesheetdemo_img, player_one_steps)
player_2 = Player(700, 310)

#game loop
run = True

while run:
    clock.tick(FPS)
    draw_bg()

    health_bar(player_1.health, 20, 20)
    health_bar(player_2.health, 580, 20)


    player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2)
    #player_2.move()

    # draw players
    player_1.draw(screen)
    player_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()