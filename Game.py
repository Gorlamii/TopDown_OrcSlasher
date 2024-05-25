"""IMPORTS"""
import os

import Characters
from SETTINGS import *
from Characters import Player
import random

pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self, camera_width, camera_height, camera_speed, fps, screen_colour, world_width, world_height):

        """Game Settings"""
        self.pause_game = False
        # World Settings
        self.world_width = world_width
        self.world_height = world_height
        self.world = pygame.Surface((self.world_width, self.world_height))
        self.spawn_locations = [
            [(self.world_width // 2, 0), 'top'],  # Top Center
            [(self.world_width // 2, self.world_height), 'midbottom'],  # Bottom Center
            [(self.world_width, self.world_height // 2), 'right'],  # Right Center
            [(0, self.world_height // 2), 'left']  # Left Center
        ]

        """Music Settings"""
        self.bg_song = pygame.mixer.Sound(BG_SONG)
        self.bg_song.set_volume(0.15)
        # Camera Settings
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.camera_speed = camera_speed
        self.camera = pygame.Rect(0, 0, self.camera_width, self.camera_height)
        # Set display
        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        # General Game properties
        self.running = True
        self.bg_image = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        self.bg_size = self.bg_image.get_size()
        # Screen Settings
        self.fps = fps
        self.screen_colour = screen_colour

        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_NAME)

        """Enemy Waves"""
        self.wave_count = 1

        """Player Character"""
        self.player_group = pygame.sprite.Group()
        # Get Sprites in list
        self.player_idle_sprites = []
        # Open iterate over file adding each image to the list
        for filename in os.listdir(PLAYER_IDLE_SPRITES_PATH):
            sprite = pygame.image.load(f'{os.path.join(PLAYER_IDLE_SPRITES_PATH, filename)}').convert_alpha()
            self.player_idle_sprites.append(sprite)
        self.player = Player(PLAYER_SPEED,
                             self.player_idle_sprites, PLAYER_HEALTH, PLAYER_STAMINA,
                             self.world, self.camera, self.clock)
        # noinspection PyTypeChecker
        self.player_group.add(self.player)

        """Enemy Characters"""
        self.orc_group = pygame.sprite.Group()
        self.orc_idle_sprites = []
        # Add all paths to images as loaded images
        for filename in os.listdir(ORC_IDLE_SPRITES_PATH):
            sprite = pygame.image.load(f'{os.path.join(ORC_IDLE_SPRITES_PATH, filename)}').convert_alpha()
            self.orc_idle_sprites.append(sprite)

        # Cursor Position
        self.cursor_pos = (0, 0)

    # Event Handler
    def events(self):
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Player Movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pause_game = False
            self.player.rect.x -= self.player.speed
        if keys[pygame.K_RIGHT]:
            self.pause_game = False
            self.player.rect.x += self.player.speed
        if keys[pygame.K_UP]:
            self.pause_game = False
            self.player.rect.y -= self.player.speed
        if keys[pygame.K_DOWN]:
            self.pause_game = False
            self.player.rect.y += self.player.speed
        # Check to pause game
        if keys[pygame.K_SPACE]:
            self.pause_game = not self.pause_game
        # Check for player attacks
        if keys[pygame.K_f]:
            if current_time - self.player.last_attack_time > self.player.attack_cooldown:
                self.player.last_attack_time = current_time
                hit_rect = self.player.detection_box()
                temp_rect_sprite = RectSprite(hit_rect)
                collided_orcs = pygame.sprite.spritecollide(temp_rect_sprite,
                                                            self.orc_group, dokill=False)
                for orc in collided_orcs:
                    orc.health -= PLAYER_DAMAGE
                    print('Hit Orc!', orc, sep='\n')

    # Update Method
    def update(self):
        if not self.pause_game:
            self.camera.center = self.player.rect.midright

            # Ensure camera in world boundaries
            if self.camera.left < 0:
                self.camera.left = 0
            if self.camera.right > self.world_width:
                self.camera.right = self.world_width
            if self.camera.top < 0:
                self.camera.top = 0
            if self.camera.bottom > self.world_height:
                self.camera.bottom = self.world_height

            # Update Player Character
            self.player.update()
            # Update all Orcs
            for orc in self.orc_group:
                if orc.health <= 0:
                    orc.kill()

            self.orc_group.update()

            # Gradual spawning of orcs
            if len(self.orc_group) < WAVE_MODIFIERS[self.wave_count]:
                for i in range(WAVE_MODIFIERS[self.wave_count]):  # Cap the orcs per wave
                    orc = Characters.EnemyOrc(ORC_SPEED, self.orc_idle_sprites,
                                              ORC_HEALTH, ORC_STAMINA,
                                              self.world, self.clock, self.player, self.orc_group,
                                              self.spawn_locations[random.randint(0, 3)][random.randint(0, 1)])
                    # noinspection PyTypeChecker
                    self.orc_group.add(orc)
                    print(len(self.orc_group))

        # Check Orc collisions
        for sprite in self.orc_group.sprites():
            if pygame.sprite.spritecollideany(sprite, self.player_group):
                pass

    # Render Method
    def render(self):
        if self.pause_game:
            # Render the pause message
            font = pygame.font.Font(PAUSE_FONT, 70)
            pause_text = font.render('PAUSED', True, BLACK)
            self.screen.blit(pause_text, (
                self.camera_width // 2 - pause_text.get_width() // 2,
                self.camera_height // 2 - pause_text.get_height() // 2))
            pygame.display.flip()
            return  # Exit early when paused
        # Background onto World Surface
        for x in range(0, self.world_width, self.bg_size[0]):  # Steps of The width of image
            for y in range(0, self.world_height, self.bg_size[1]):  # Steps of vert length of image
                self.world.blit(self.bg_image, (x, y))

        self.player.render()

        # Print all orcs
        for orc in self.orc_group:
            orc.render()

        # blit matched camera portion from World onto Display surface
        self.screen.blit(self.world, (0, 0), self.camera)

        pygame.display.flip()

    # Compile Method - runs everything
    def run(self):
        self.bg_song.play(loops=-1)

        while self.running:
            self.cursor_pos = pygame.mouse.get_pos()

            self.events()
            self.update()
            self.render()

            self.clock.tick(SCREEN_FPS)
            pygame.display.update()

        pygame.quit()


game = Game(CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_SPEED,
            SCREEN_FPS, BLACK,
            WORLD_WIDTH, WORLD_HEIGHT)
game.run()
