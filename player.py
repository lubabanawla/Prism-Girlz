import pygame
import pygame.draw

class Player():
    def __init__(self, x, y, data, sprite_sheet, animation_steps):
        self.size = data
        self.image_scale = data[1]
        self.flip = False
        self.action = 0 # what the player doing
        # 0 is idle, 1 is run, 2 is jump, 3 the attack, 5 hit, 6 death
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        if self.action == 0:
            sprite_sheet = sprite_sheet[1]
        if self.action == 1:
            sprite_sheet = sprite_sheet[2]
        if self.action == 3:
            sprite_sheet = sprite_sheet[0]
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attack_type = 0
        self.attacking = False
        self.health = 100

    def load_images(self, sprite_sheets, animation_steps):
        animation_list = []
        for sheet, steps in zip(sprite_sheets, animation_steps):
            animation_frames = []
            for frame in range(steps):
                image = self.get_image(sheet, frame)
                animation_frames.append(image)
            animation_list.append(animation_frames)
        return animation_list

    def get_image(self, sheet, frame):
        width = sheet.get_width() // 5
        height = sheet.get_height()
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(sheet, (0, 0), (frame * width, 0, width, height))

        return image

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, surface, enemy):
        speed = 10
        change_x = 0
        change_y = 0
        gravity = 2

        key = pygame.key.get_pressed()

        # check for movement and NOT when attacking
        if not self.attacking:
            if key[pygame.K_a]:
                self.action = 1  # Run
                change_x = -speed
            elif key[pygame.K_d]:
                self.action = 1  # Run
                change_x = speed
            else:
                self.action = 0  # Idle

            if key[pygame.K_w] and self.jump == False:
                self.jump = True
                self.vel_y = -30

            #attack
            if key[pygame.K_f]:
                self.attack(surface, enemy)


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
        self.action = 3  # Attack
        self.attacking = True
        self.frame_index = 0
        collision_attack = pygame.Rect((self.rect.centerx - (2*self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height))
        if collision_attack.colliderect(enemy.rect):
            enemy.health -= 10
            # add movement after attack

        pygame.draw.rect(surface, (0, 0, 255), collision_attack)

    def draw(self, surface):
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        #surface.blit(self.image, (self.rect.x, self.rect.y))
        self.update_animation()
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, (self.rect.x, self.rect.y))

    def update_animation(self):
        animation_cooldown = 100  # Milliseconds
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action == 3:  # Attack animation ends
                    self.attacking = False
                    self.action = 0  # Back to idle
            self.image = self.animation_list[self.action][self.frame_index]
