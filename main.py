import pygame
from player import Player
import spritesheet

pygame.init()

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

def health_bar(health, x, y):
    update_health = health / 100
    pygame.draw.rect(screen, (0, 0, 0), (x-1, y-1, 403, 33))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 400, 30))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 400 * update_health, 30))

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prism Girlz")

#frame rate
clock = pygame.time.Clock()
FPS = 60

# set icon for pygame
pygame_icon = pygame.image.load("assets/images/icons/prismgirlzicon.png")
pygame.display.set_icon(pygame_icon)

# player variables for spritesheet
player_size = 292
player_scale = 4
player_offset = [72, 56]
player_data = [player_size, player_scale, player_offset]


# bg image
bg_image = pygame.image.load("prismgirlz.png")

# load sprite sheets
playeroneatksheet = spritesheet.spritesheet("assets/images/spritesheets/playerone/playeroneatk.png")
playeroneidlesheet = spritesheet.spritesheet("assets/images/spritesheets/playerone/playeroneidle.png")
playeronerunsheet = spritesheet.spritesheet("assets/images/spritesheets/playerone/playeronerun.png")
playeronespritesheet = [playeroneidlesheet, playeronerunsheet, playeroneatksheet]
# animation
playeronesteps = [5, 6, 5]

playertwoidlesheet = pygame.image.load("assets/images/spritesheets/playertwo/playertwoidle.png").convert_alpha()
playertwospritesheet = [playertwoidlesheet, playeronerunsheet, playeroneatksheet]
playertwosteps = [5, 6, 5]

# create two instances of the players
player_1 = Player(200, 310, player_data, playeronespritesheet, playeronesteps)
player_2 = Player(700, 310, player_data, playertwospritesheet, playertwosteps)

# load BG music
pygame.mixer.music.load("assets/sounds/music/fridaytheme.mp3")
# change volume
initial_volume = 0.3
pygame.mixer.music.set_volume(initial_volume)
# play the BG music
pygame.mixer.music.play(-1, 0.0)
# delay music (?) might delete this
pygame.time.delay(500)

# game loop
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
            pygame.mixer.music.stop()

    pygame.display.update()

pygame.quit()