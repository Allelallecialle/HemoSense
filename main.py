import pygame
import sys
import math
from game_config import *
import Balloon, TargetBand, hand_input

#Credits for sliding to russ123's github repo: https://github.com/russs123/pygame_tutorials/blob/main/Infinite_Background/scroll_tut.py


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Glide")
clock = pygame.time.Clock()

balloon = Balloon.Balloon()
target = TargetBand.TargetBand()

score = 0

font = pygame.font.SysFont("Verdana", 32)

bg = pygame.image.load("./images/cloud_background_cropped.jpg").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()
# define game variables
scroll = 0
tiles = math.ceil(WIDTH / bg_width) + 1
running = True
while running:
    clock.tick(FPS)

    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        bg_rect.x = i * bg_width + scroll

    # scroll background
    scroll -= 5

    # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    # --- Update ---
    hand_state = hand_input.get_hand_state()  # integrate mediapipe here!
    balloon.update(hand_state)
    target.update()

    # scoring
    band_top = target.center_y - TARGET_BAND_HEIGHT // 2
    band_bottom = target.center_y + TARGET_BAND_HEIGHT // 2
    if band_top < balloon.y < band_bottom:
        score += 1/(FPS*0.5)  # to increment keep the air balloon inside for long enough


    target.draw(screen)
    balloon.draw(screen)

    # score display
    score_text = font.render(f"Score: {int(score)}", True, (50, 50, 80))
    screen.blit(score_text, (20, 20))

    pygame.display.update()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
sys.exit()
