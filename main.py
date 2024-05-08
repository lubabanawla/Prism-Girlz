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

# bg image
bg_image = pygame.image.load("backgroundimage.jpeg")
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# create two instances of fighter
player_1 = Player(200, 310)
player_2 = Player(700, 310)

#game loop
run = True

while run:
    clock.tick(FPS)
    draw_bg()

    player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
    #player_2.move()

    # draw players
    player_1.draw(screen)
    player_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()