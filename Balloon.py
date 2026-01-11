from game_config import *
import pygame

class Balloon:
    def __init__(self):
        self.x = BALLOON_X
        self.y = BALLOON_START_Y
        self.velocity = 0

    def update(self, state):
        if state == "squeeze":
            self.velocity -= ASCENT_SPEED

        # gravity that always pulls down
        self.velocity += GRAVITY
        #simulate air resistance
        self.velocity = self.velocity * DAMPING

        #update position
        self.y += self.velocity

        if self.y < BALLOON_HEIGHT:
            self.y = BALLOON_HEIGHT
            self.velocity = 0
        if self.y > HEIGHT - BALLOON_HEIGHT:
            self.y = HEIGHT - BALLOON_HEIGHT
            self.velocity = 0

    def draw(self, screen):
        balloon_img = pygame.image.load("./images/air_balloon.svg")
        balloon_img_scaled = pygame.transform.scale(balloon_img, (BALLOON_WIDTH, BALLOON_HEIGHT))
        screen.blit(balloon_img_scaled, (self.x, int(self.y)))

