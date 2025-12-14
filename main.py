import pygame
import sys
import time
from game_config import *
import Balloon, TargetBand, hand_input



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Glide")
clock = pygame.time.Clock()

balloon = Balloon.Balloon()
target = TargetBand.TargetBand()

score = 0

font = pygame.font.SysFont("Verdana", 32)

running = True
while running:
    screen.fill((240, 245, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    hand_state = hand_input.get_hand_state()  # integrate mediapipe here!
    balloon.update(hand_state)
    target.update()

    # scoring
    band_top = target.center_y - TARGET_BAND_HEIGHT // 2
    band_bottom = target.center_y + TARGET_BAND_HEIGHT // 2
    if band_top < balloon.y < band_bottom:
        score += 1/(FPS*0.5)  # increment slowly

    # --- Draw ---
    target.draw(screen)
    balloon.draw(screen)

    # score display
    score_text = font.render(f"Score: {int(score)}", True, (50, 50, 80))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
