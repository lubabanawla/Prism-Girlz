import pygame
import cv2
import sys
from player import Player
from gameround import GameRound
pygame.init()

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

def health_bar(health, x, y):
    update_health = health / 100
    pygame.draw.rect(screen, (0, 0, 0), (x-1, y-1, 403, 33))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 400, 30))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 400 * update_health, 30))

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

video_path = 'PRIZM GIRLZ.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    sys.exit()

video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

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
player_data = [player_size, player_scale]

# bg image
bg_image = pygame.image.load("prismgirlz.png")
#load vicory image
victory_img = pygame.image.load("victory.png").convert_alpha()

# create two instances of the players
player_1 = Player(1, 200, 310, False, player_data)
player_2 = Player(2, 700, 310, True, player_data)

video_boolean = True

# load video music
if video_boolean:
    pygame.mixer.music.load("PRIZM GIRLZ.mp3")
    # change volume
    initial_volume = 0.3
    pygame.mixer.music.set_volume(initial_volume)
    # play the BG music
    pygame.mixer.music.play(-1, 0.0)

# game loop
run = True
frame_time = 300  # 300 milliseconds
last_frame_update = pygame.time.get_ticks()
current_time = pygame.time.get_ticks()
clock = pygame.time.Clock()

count_font = pygame.font.SysFont("Arial", 80)
score_font = pygame.font.SysFont("Arial", 30)

# create a GameRound instance
game_round = GameRound(screen, count_font, score_font, victory_img)

# Play video first
def play_video(cap):
    while cap.isOpened():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cap.release()
                return False

        ret, frame = cap.read()
        if not ret:
            return False  # End of video

        # Convert frame to Pygame surface
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Display frame
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        # Control frame rate
        clock.tick(fps)

    cap.release()
    return True and video_boolean == False

# Play the video
if play_video(cap):
    # Play background music after video ends
    pygame.mixer.music.stop()

while run:
    pygame.mixer.music.stop()

    clock.tick(FPS)
    draw_bg()
    # show player stats
    game_round.draw_scores()
    print(player_1.attack_cooldown)

    health_bar(player_1.health, 20, 20)
    health_bar(player_2.health, 580, 20)

    if game_round.intro_count <= 0:
        # move fighters
        player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2)
        player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1)
    else:
        # display count timer
        game_round.draw_intro_count(SCREEN_WIDTH, SCREEN_HEIGHT)

    # draw players
    player_1.draw(screen)
    player_2.draw(screen)

    current_time = pygame.time.get_ticks()
    if current_time - last_frame_update > frame_time:
        player_1.next_frame()
        player_2.next_frame()
        last_frame_update = current_time

        # Check if the round is over
    if game_round.check_round_over(player_1, player_2):
        player_1 = Player(1, 200, 310, False, player_data)
        player_2 = Player(2, 700, 310, True, player_data)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.mixer.music.stop()

    pygame.display.update()

pygame.quit()