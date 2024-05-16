import pygame
import pygame.draw


class Player():
    def __init__(self, x, y, data, sprite_sheet, animation_steps):
        self.size = data
        self.image_scale = data[1]
        self.flip = False
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # what is the player doing
        # 0 is idle, 1 is run, 2 is jump, 3 and 4 r the attack, 5 hit, 6 death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attack_type = 0
        self.attacking = False
        self.health = 100

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            # i could also do y=0 and then y+=1 after an animation
            temporary_img_list = []
            for x in range(animation):
                max_x = sprite_sheet.get_width() // self.size[0] - 1
                max_y = sprite_sheet.get_height() // self.size[1] - 1

                clamped_x = min(x, max_x)
                clamped_y = min(y, max_y)

                temporary_img = sprite_sheet.subsurface(clamped_x * self.size[0], clamped_y * self.size[1], self.size[0],
                                                    self.size[1])
                #pygame.transform.scale(temporary_img, (self.size * self.image_scale, self.size * self.image_scale))
                new_size = (int(self.size[0] * self.image_scale), int(self.size[1] * self.image_scale))
                pygame.transform.scale(temporary_img, new_size)
                #temporary_img = sprite_sheet.subsurface(x * self.size[0], y * self.size[1], self.size[0], self.size[1])
                temporary_img_list.append(temporary_img)
            animation_list.append(temporary_img_list)
        return animation_list
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
        surface.blit(self.image, (self.rect.x, self.rect.y))
