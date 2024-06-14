import pygame

class GameRound:
    def __init__(self, screen, count_font, score_font, victory_img):
        self.screen = screen
        self.count_font = count_font
        self.score_font = score_font
        self.victory_img = victory_img
        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]  # player scores. [P1, P2]
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000
        self.round_over_time = None

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_scores(self):
        self.draw_text("P1: " + str(self.score[0]), self.score_font, (255, 0, 0), 20, 60)
        self.draw_text("P2: " + str(self.score[1]), self.score_font, (255, 0, 0), 580, 60)

    def draw_intro_count(self, screen_width, screen_height):
        if self.intro_count > 0:
            self.draw_text(str(self.intro_count), self.count_font, (255, 0, 0), screen_width / 2, screen_height / 3)
            if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                self.intro_count -= 1
                self.last_count_update = pygame.time.get_ticks()

    def check_round_over(self, player_1, player_2):
        if not self.round_over:
            if not player_1.alive:
                self.score[1] += 1
                self.round_over = True
                self.round_over_time = pygame.time.get_ticks()
            elif not player_2.alive:
                self.score[0] += 1
                self.round_over = True
                self.round_over_time = pygame.time.get_ticks()
        else:
            self.screen.blit(self.victory_img, (360, 150))
            if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                self.round_over = False
                self.intro_count = 3
                return True  # Indicate that a new round should start
        return False

