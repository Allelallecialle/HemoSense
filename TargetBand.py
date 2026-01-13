from game_config import *
import pygame
import math

class TargetBand:
    def __init__(self):
        self.center_y = HEIGHT // 2
        self.time = 0.0
        self.angular_speed = 2 * math.pi / TARGET_PERIOD

    def update(self, dt):
        self.time += dt
        self.center_y = (HEIGHT // 2 + math.sin(self.angular_speed * self.time) * TARGET_AMPLITUDE)

    def draw(self, screen):
        top = int(self.center_y - TARGET_BAND_HEIGHT // 2)
        pygame.draw.rect(
            screen,
            (180, 220, 255),
            (0, top, WIDTH, TARGET_BAND_HEIGHT),
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (100, 150, 200),
            (0, top, WIDTH, TARGET_BAND_HEIGHT),
            4
        )
