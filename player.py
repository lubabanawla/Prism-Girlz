import pygame
import pygame.draw


class Player():
    def __init__(self, x, y):
        self.flip = False
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attack_type = 0
        self.attacking = False
        self.health = 100

    def load_images(self, sprite_sheet, animation_steps):
        for i in range(animation):
            temporary_img = sprite_sheet.subsurface()
    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, surface, enemy):
        speed = 10
        change_x = 0
        change_y = 0
        gravity = 2

        key = pygame.key.get_pressed()

        # check for movement and NOT when attacking
        if self.attacking == False:
            if key[pygame.K_a]:
                change_x = -speed
            if key[pygame.K_d]:
                change_x = speed
            if key[pygame.K_w] and self.jump == False:
                self.jump = True
                self.vel_y = -30

            #attack
            if key[pygame.K_f] or key[pygame.K_g]:
                self.attack(surface, enemy)
                if key[pygame.K_f]:
                    self.attack_type = 1
                elif key[pygame.K_g]:
                    self.attack_type = 2

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

        # make sure the players face eachother
        if enemy.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # updating the position
        self.rect.x += change_x
        self.rect.y += change_y

    def attack(self, surface, enemy):
        self.attacking = True
        collision_attack = pygame.Rect((self.rect.centerx - (2*self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height))
        if collision_attack.colliderect(enemy.rect):
            enemy.health -= 10


        pygame.draw.rect(surface, (0, 0, 255), collision_attack)



    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

