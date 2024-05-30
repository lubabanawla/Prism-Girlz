import pygame
import pygame.draw

class Player():
    def __init__(self, player, x, y, data):
        self.player = player
        self.size = data
        self.image_scale = data[1]
        self.flip = False
        self.offset = data[2]
        self.action = 0 # what the player doing
        # 0 is idle, 1 is run, 2 is jump, 3 the attack, 5 hit, 6 death
        self.frame_index = 0
        self.image = 0
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attack_type = 0
        self.attacking = False
        self.health = 100

        # Load and scale images
        self.player_one_idle = [
            self.scale_image(pygame.image.load(f"assets/images/playerone/idle/Blue_Idle_{i}.png").convert_alpha())
            for i in range(1, 6)
        ]

        self.player_two_idle = [
            self.scale_image(pygame.image.load(f"assets/images/playertwo/idle/Pink_Idle_{i}.png").convert_alpha())
            for i in range(1, 5)
        ]

        self.current_frame = 0

    def scale_image(self, image):
        return pygame.transform.scale(image,(image.get_width() * self.image_scale, image.get_height() * self.image_scale))
    def get_image(self):
        if self.player == 1:
            return self.player_one_idle[self.current_frame]
        if self.player == 2:
            return self.player_two_idle[self.current_frame]

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, surface, enemy):
        speed = 10
        change_x = 0
        change_y = 0
        gravity = 2

        key = pygame.key.get_pressed()

        # check for movement and NOT when attacking
        if not self.attacking:
            if self.player == 1:
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

            if self.player == 2:
                if key[pygame.K_LEFT]:
                    self.action = 1  # Run
                    change_x = -speed
                elif key[pygame.K_RIGHT]:
                    self.action = 1  # Run
                    change_x = speed
                else:
                    self.action = 0  # Idle

                if key[pygame.K_UP] and self.jump == False:
                    self.jump = True
                    self.vel_y = -30

                #attack
                if key[pygame.K_l]:
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

    def next_frame(self):
        self.current_frame += 1
        if self.current_frame == len(self.player_one_idle):
            self.current_frame = 0
        if self.current_frame == len(self.player_two_idle):
            self.current_frame = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

        #flipped_image = pygame.transform.flip(self.get_image(), self.flip, False)
        #surface.blit(flipped_image, (self.rect.x, self.rect.y))

        img = pygame.transform.flip(self.get_image(), self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))





