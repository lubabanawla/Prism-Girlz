import pygame
from player import Player

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
player_scale = 1
player_offset = [10, 15]
player_data = [player_size, player_scale, player_offset]

# bg image
bg_image = pygame.image.load("prismgirlz.png")

# load player one images
p1_atk_1 = pygame.image.load("assets/images/playerone/atk/Blue_ATK_1.png").convert_alpha()
p1_atk_2 = pygame.image.load("assets/images/playerone/atk/Blue_ATK_2.png").convert_alpha()
p1_atk_3 = pygame.image.load("assets/images/playerone/atk/Blue_ATK_3.png").convert_alpha()
p1_atk_4 = pygame.image.load("assets/images/playerone/atk/Blue_ATK_4.png").convert_alpha()
p1_atk_5 = pygame.image.load("assets/images/playerone/atk/Blue_ATK_5.png").convert_alpha()
player_one_atk = [p1_atk_1, p1_atk_2, p1_atk_3, p1_atk_4, p1_atk_5]

p1_idle_1 = pygame.image.load("assets/images/playerone/idle/Blue_Idle_1.png").convert_alpha()
p1_idle_2 = pygame.image.load("assets/images/playerone/idle/Blue_Idle_2.png").convert_alpha()
p1_idle_3 = pygame.image.load("assets/images/playerone/idle/Blue_Idle_3.png").convert_alpha()
p1_idle_4 = pygame.image.load("assets/images/playerone/idle/Blue_Idle_4.png").convert_alpha()
p1_idle_5 = pygame.image.load("assets/images/playerone/idle/Blue_Idle_5.png").convert_alpha()
player_one_idle = [p1_idle_1, p1_idle_2, p1_idle_3, p1_idle_4, p1_idle_5]

p1_run_1 = pygame.image.load("assets/images/playerone/run/Blue_Run_1.png").convert_alpha()
p1_run_2 = pygame.image.load("assets/images/playerone/run/Blue_Run_2.png").convert_alpha()
p1_run_3 = pygame.image.load("assets/images/playerone/run/Blue_Run_3.png").convert_alpha()
p1_run_4 = pygame.image.load("assets/images/playerone/run/Blue_Run_4.png").convert_alpha()
p1_run_5 = pygame.image.load("assets/images/playerone/run/Blue_Run_5.png").convert_alpha()
p1_run_6 = pygame.image.load("assets/images/playerone/run/Blue_Run_6.png").convert_alpha()
player_one_run = [p1_run_1, p1_run_2, p1_run_3, p1_run_4, p1_run_5, p1_run_6]

# load player two images
p2_idle_1 = pygame.image.load("assets/images/playertwo/idle/Pink_Idle_1.png").convert_alpha()
p2_idle_2 = pygame.image.load("assets/images/playertwo/idle/Pink_Idle_2.png").convert_alpha()
p2_idle_3 = pygame.image.load("assets/images/playertwo/idle/Pink_Idle_3.png").convert_alpha()
p2_idle_4 = pygame.image.load("assets/images/playertwo/idle/Pink_Idle_4.png").convert_alpha()
player_two_idle = [p2_idle_1, p2_idle_2, p2_idle_3, p2_idle_4]

# create two instances of the players
player_1 = Player(1, 200, 310, False, player_data)
player_2 = Player(2, 700, 310, True, player_data)

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
frame_time = 300  # 300 milliseconds
last_frame_update = pygame.time.get_ticks()

while run:
    clock.tick(FPS)
    draw_bg()

    health_bar(player_1.health, 20, 20)
    health_bar(player_2.health, 580, 20)

    player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2)
    player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1)

    # draw players
    player_1.draw(screen)
    player_2.draw(screen)

    current_time = pygame.time.get_ticks()
    if current_time - last_frame_update > frame_time:
        player_1.next_frame()
        player_2.next_frame()
        last_frame_update = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.mixer.music.stop()

    pygame.display.update()

pygame.quit()