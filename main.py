import pygame
import sys
import math
from game_config import *
import Balloon, TargetBand, hand_input, introduction_screen, fainting_simulation
import threading
from arduino_sketch.serial_port_setup import arduino_disconnect, arduino_connection

#Credits for sliding to russ123's github repo: https://github.com/russs123/pygame_tutorials/blob/main/Infinite_Background/scroll_tut.py


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Glide")
clock = pygame.time.Clock()


# --- START HAND TRACKING THREAD ---
hand_thread = threading.Thread(
    target=hand_input.capture_from_camera,
    daemon=True
)
hand_thread.start()
#--------- CALL ARDUINO SETUP -------------
arduino = arduino_connection()

#--- PYGAME VIDEOGAME SECTION ---
balloon = Balloon.Balloon()
target = TargetBand.TargetBand()
game_start_time = pygame.time.get_ticks()

score = 0
start_time = 0

font = pygame.font.SysFont("Verdana", 32)

bg = pygame.image.load("./images/cloud_background_cropped.jpg").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()
# define game variables
scroll = 0
tiles = math.ceil(WIDTH / bg_width) + 1

trigger_fainting = False

#start introduction
introduction_screen.show_instruction_screen(screen, clock)

running = True
while running:
    clock.tick(FPS)
    dt = clock.tick(FPS) / 1000.0

    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        bg_rect.x = i * bg_width + scroll

    # scroll background
    scroll -= 5

    # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    balloon.update(hand_input.CURRENT_HAND_STATE)  # mediapipe input
    target.update(dt)

    # scoring: to increment the score keep the air balloon in the target zone for at least 5s
    band_top = target.center_y - TARGET_BAND_HEIGHT // 2
    band_bottom = target.center_y + TARGET_BAND_HEIGHT // 2
    # counter_score to count the seconds inside the target band
    #TODO check if it's ok
    if band_top <= balloon.y + BALLOON_HEIGHT and  balloon.y - BALLOON_HEIGHT <= band_bottom:
        if start_time == 0:
            start_time = pygame.time.get_ticks()
        else:
            current_time = pygame.time.get_ticks()
            time_passed = (current_time - start_time) / 1000
            print(time_passed)
            if time_passed >= 5:
                score += 1
                start_time = 0
                current_time = 0
                time_passed = 0
    else:
        start_time = 0
        current_time = 0
        time_passed = 0

    target.draw(screen)
    balloon.draw(screen)

    # score display
    score_text = font.render(f"Score: {int(score)}", True, (50, 50, 80))
    screen.blit(score_text, (20, 20))

    pygame.display.update()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # to trigger a fainting simulation. In real case scenario we would have the alarm to physicians
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                trigger_fainting = True
                fainting_simulation.simulation_fainting(trigger_fainting, screen, clock, arduino)
                arduino = arduino_disconnect(arduino)
                running = False
            #TODO: fix close fainting

    # Automatically stop the game after 10 AMT repetitions (i.e. 10s*10=100s)
    if pygame.time.get_ticks() - game_start_time > GAME_DURATION:
        running = False

pygame.quit()
sys.exit()
