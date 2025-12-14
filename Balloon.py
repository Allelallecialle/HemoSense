from game_config import *
import pygame

class Balloon:
    def __init__(self):
        self.x = BALLOON_X
        self.y = BALLOON_START_Y
        self.velocity = 0

    def update(self, state):
        # state: "squeeze" or "release"

        if state == "squeeze":
            self.velocity -= ASCENT_SPEED
        else:
            self.velocity += DESCENT_SPEED

        # gravity stabilizes motion
        self.velocity += GRAVITY * 0.2

        self.y += self.velocity

        # clamp to window
        if self.y < BALLOON_RADIUS:
            self.y = BALLOON_RADIUS
            self.velocity = 0
        if self.y > HEIGHT - BALLOON_RADIUS:
            self.y = HEIGHT - BALLOON_RADIUS
            self.velocity = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 100, 100), (self.x, int(self.y)), BALLOON_RADIUS)
        pygame.draw.line(screen, (100, 80, 80),
                         (self.x, int(self.y + BALLOON_RADIUS)),
                         (self.x - 10, int(self.y + BALLOON_RADIUS + 40)), 4)
        pygame.draw.line(screen, (100, 80, 80),
                         (self.x, int(self.y + BALLOON_RADIUS)),
                         (self.x + 10, int(self.y + BALLOON_RADIUS + 40)), 4)

