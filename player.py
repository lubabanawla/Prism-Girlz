import pygame
import pygame.draw


class Player():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attack = 0

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, surface):
        speed = 10
        change_x = 0
        change_y = 0
        gravity = 2

        key = pygame.key.get_pressed()
        # check for movement
        if key[pygame.K_a]:
            change_x = -speed
        if key[pygame.K_d]:
            change_x = speed
        if key[pygame.K_w] and self.jump == False:
            self.jump = True
            self.vel_y = -30

        #attack
        if key[pygame.K_f] or key[pygame.K_g]:
            self.attack(surface)
            if key[pygame.K_f]:
                self.attack = 1
            elif key[pygame.K_g]:
                self.attack = 2

        self.vel_y += gravity
        change_y += self.vel_y

        # stays on screen
        if self.rect.left + change_x < 0:
            change_x = -self.rect.left
        elif self.rect.right + change_x > SCREEN_WIDTH:
            change_x = SCREEN_WIDTH - self.rect.right

        if self.rect.bottom + change_y > SCREEN_HEIGHT - 110:
            self.vel_y = 0
            self.jump = False
            change_y = (SCREEN_HEIGHT - 110) - self.rect.bottom

        # updating the position
        self.rect.x += change_x
        self.rect.y += change_y

    def attack(self, surface):
        collision_attack = self.Rect(self.rect.centerx, self.rect.centery, 2 * self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (0, 0, 255), collision_attack)


    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

