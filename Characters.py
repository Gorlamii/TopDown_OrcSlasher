import pygame
from SETTINGS import *
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, speed, sprite_set, health, stamina, world, camera, clock):
        pygame.sprite.Sprite.__init__(self)

        # Game settings
        self.world = world
        self.camera = camera
        self.clock = clock
        # Player Settings
        self.speed = speed
        self.sprite_set = sprite_set
        self.health = health
        # Recs and surface
        self.stamina = stamina
        self.rect = self.sprite_set[0].get_rect()
        self.rect.center = self.world.get_rect().center
        # Animation settings
        self.current_frame = 0
        self.time_last_frame = 0
        self.frame_duration = SCREEN_FPS * 6
        self.current_sprite = self.sprite_set[self.current_frame]
        # Direction Flag
        self.facing_left = False
        # Attack Timers
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.last_attack_time = 0

    def detection_box(self):
        # Size of hit area
        detection_width, detection_height = PLAYER_DETECTION_WIDTH, PLAYER_DETECTION_HEIGHT
        # If facing right
        if not self.facing_left:
            return pygame.Rect(self.rect.right, self.rect.centery - detection_height // 2,
                               detection_width, detection_height)
        elif self.facing_left:
            return pygame.Rect(self.rect.left - detection_width, self.rect.centery - detection_height // 2,
                               detection_width, detection_height)
        return None

    def update(self):
        # Ensure character is in boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WORLD_HEIGHT:
            self.rect.bottom = WORLD_HEIGHT

        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_frame >= self.frame_duration:
            self.time_last_frame = current_time
            self.current_frame = (self.current_frame + 1) % len(self.sprite_set)

        # Moving left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            self.facing_left = False

        self.current_sprite = self.sprite_set[self.current_frame]
        if self.facing_left:
            self.current_sprite = pygame.transform.flip(self.current_sprite, 1, 0)

    def render(self):
        """Animations"""
        self.world.blit(pygame.transform.scale(self.current_sprite, (PLAYER_SCALE, PLAYER_SCALE)), self.rect.topleft)


class EnemyOrc(pygame.sprite.Sprite):
    def __init__(self, speed, sprite_set, health, stamina, world, clock, player, orc_group, spawn_locations):
        pygame.sprite.Sprite.__init__(self)

        # World settings
        self.world = world
        self.clock = clock
        self.player = player
        self.orc_group = orc_group
        self.orc_group_rects = [orc.rect for orc in self.orc_group]
        self.spawn_locations = spawn_locations
        # EnemyOrc Settings
        self.speed = speed
        self.sprite_set = sprite_set
        self.health = health
        self.stamina = stamina
        # Recs and Surface
        self.rect = self.sprite_set[0].get_rect()
        # Animation settings
        self.current_frame = 0
        self.time_last_frame = 0
        self.frame_duration = SCREEN_FPS * 6
        self.current_sprite = self.sprite_set[self.current_frame]
        # Direction Flag
        self.facing_left = False

    def find_player(self):
        # Simple move to player pos without push radius
        player_pos = self.player.rect.center
        # To the left
        if player_pos[0] < self.rect.x - ORC_HIT_RANGE:
            self.rect.x -= self.speed
            if not self.facing_left:
                self.facing_left = True
        # To the right
        elif player_pos[0] > self.rect.x + ORC_HIT_RANGE:
            self.rect.x += self.speed
            if self.facing_left:
                self.facing_left = False

        # Above
        if player_pos[1] < self.rect.y - ORC_HIT_RANGE:
            self.rect.y -= self.speed
        # Below
        elif player_pos[1] > self.rect.y + ORC_HIT_RANGE:
            self.rect.y += self.speed

    def update(self):
        # Ensure orc is in boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WORLD_HEIGHT:
            self.rect.bottom = WORLD_HEIGHT

        # Check for collisions with other orcs
        for other_orc in self.orc_group:
            if other_orc != self and self.rect.colliderect(other_orc.rect):
                # Resolve collision by moving away from the other orc
                pos_diff_x = other_orc.rect.x - self.rect.x
                pos_diff_y = other_orc.rect.y - self.rect.y

                self.rect.x -= pos_diff_x
                self.rect.y -= pos_diff_y
                break  # Only resolve one collision at a time
        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_frame >= self.frame_duration:
            self.time_last_frame = current_time
            self.current_frame = (self.current_frame + 1) % len(self.sprite_set)

        # Moving left or right
        self.find_player()

        self.current_sprite = self.sprite_set[self.current_frame]
        if self.facing_left:
            self.current_sprite = pygame.transform.flip(self.current_sprite, 1, 0)

    def render(self):
        self.world.blit(pygame.transform.scale(self.current_sprite, (ORC_SCALE, ORC_SCALE)), self.rect.topleft)
