from game_config import *
import pygame
import math

class TargetBand:
    def __init__(self):
        self.center_y = HEIGHT // 2
        self.offset = 0

    def update(self):
        self.offset += TARGET_OSCILLATION_SPEED
        self.center_y = HEIGHT // 2 + math.sin(self.offset / 40) * 150

    def draw(self, screen):
        top = self.center_y - TARGET_BAND_HEIGHT // 2
        pygame.draw.rect(screen, (180, 220, 255),
                         (0, top, WIDTH, TARGET_BAND_HEIGHT),
                         border_radius=10)
        pygame.draw.rect(screen, (100, 150, 200),
                         (0, top, WIDTH, TARGET_BAND_HEIGHT), 4)
