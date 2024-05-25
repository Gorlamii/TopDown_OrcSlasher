import pygame

"""HELPER FUNCTIONS"""


class RectSprite(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect


"""GENERAL GAME SETTINGS"""
GAME_NAME = 'TopDown Shooter'
BACKGROUND_IMAGE = 'AssetPacks/Background_Images/pixel_grass_1.jpg'
WAVE_MODIFIERS = {  # Wave Number : Amount to Spawn
    1: 5,
    2: 10,
    3: 20,
    4: 35,
    5: 45

}
PAUSE_FONT = 'Fonts/PixemonTrialRegular-p7nLK.ttf'
BG_SONG = 'Music/2021-08-17_-_8_Bit_Nostalgia_-_www.FesliyanStudios.com.mp3'

"""TILESET FUNCTIONALITIES"""
TILESET_PATH = 'AssetPacks/Character_Sprites/Tiny RPG Character Asset Pack v1.02 -Free Soldier&Orc/Orc/Orc/Orc-Walk.png'
CROP_TILESET_PATH = 'AssetPacks/Enemy_Characters/OrcSoldier/OrcSoldier_Idle'
BLOCK_SIZE_X = 100
BLOCK_SIZE_Y = 100

WORLD_WIDTH = 2200
WORLD_HEIGHT = 2200
SCREEN_FPS = 120

CAMERA_WIDTH = 1000
CAMERA_HEIGHT = 1000
CAMERA_SPEED = 3.5

"""Player"""
PLAYER_IDLE_SPRITES_PATH = 'AssetPacks/Player_Characters/Soldier/Soldier_Idle'
PLAYER_SPEED = 3
PLAYER_HEALTH = 100
PLAYER_STAMINA = 100
PLAYER_SCALE = 65
PLAYER_DETECTION_WIDTH = 45
PLAYER_DETECTION_HEIGHT = 20
PLAYER_DAMAGE = 20
PLAYER_ATTACK_COOLDOWN = 25

"""Enemy Orc"""
ORC_IDLE_SPRITES_PATH = 'AssetPacks/Enemy_Characters/OrcSoldier/OrcSoldier_Idle'
ORC_SPEED = 1
ORC_HEALTH = 100
ORC_STAMINA = 30
PUSH_RADIUS = 250
ORC_SCALE = 70
ORC_HIT_RANGE = 60
MAX_ORCS_PER_WAVE = 20

""" DEFAULT COLOURS"""
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (0, 255, 0)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
