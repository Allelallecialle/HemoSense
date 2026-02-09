import cv2
import pygame
from pygame._sdl2 import Window, Renderer, Texture
import sys
import math
from game_config import *
import Balloon, TargetBand, hand_input, introduction_screen, fainting_simulation
import threading
from arduino_sketch.serial_port_setup import arduino_disconnect, arduino_connection

#Credits for sliding background to russ123's github repo: https://github.com/russs123/pygame_tutorials/blob/main/Infinite_Background/scroll_tut.py

def run_videogame():
    pygame.init()

    # --- Pygame window for game ---
    game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Balloon Glide")
    clock = pygame.time.Clock()

    # --- SDL2 window for hand camera ---
    cam_win = Window("Hand Camera", size=(800, 550))
    cam_renderer = Renderer(cam_win)

    # --- Start hand tracking thread ---
    hand_thread = threading.Thread(
        target=hand_input.capture_from_camera,
        daemon=True
    )
    hand_thread.start()

    # --- Arduino setup---
    arduino = arduino_connection()

    # --- Game objects instantiation ---
    balloon = Balloon.Balloon()
    target = TargetBand.TargetBand()
    game_start_time = pygame.time.get_ticks()

    # --- Init for pygame music ---
    pygame.mixer.init()
    pygame.mixer.music.load('./pygame_music/08-Spring-Sunrise.mp3')
    pygame.mixer.music.play()

    #--- Define game variables ---
    score = 0
    start_time = 0
    font = pygame.font.SysFont("Verdana", 32)

    bg = pygame.image.load("./images/cloud_background_cropped.jpg").convert()
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()
    scroll = 0
    tiles = math.ceil(WIDTH / bg_width) + 1

    # Start introduction
    introduction_screen.show_instruction_screen(game_surface, clock)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Hand camera pygame window ---
        with hand_input.FRAME_LOCK:
            frame = hand_input.DEBUG_FRAME

        if frame is None:
            print("Waiting for camera frames...")

        # to show camera hand detection
        if frame is not None:
            frame_rgb = cv2.resize(frame, (800, 550))
            surface = pygame.image.frombuffer(
                frame_rgb.tobytes(),
                frame_rgb.shape[1::-1],
                "RGB"
            )
            texture = Texture.from_surface(cam_renderer, surface)
            cam_renderer.clear()
            cam_renderer.blit(texture)
            cam_renderer.present()
        # ----------------------------------------

        # --- Background code---
        # draw scrolling background
        for i in range(tiles):
            game_surface.blit(bg, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll

        # scroll background
        scroll -= 5
        # reset scroll
        if abs(scroll) > bg_width:
            scroll = 0

        # scoring: to increment the score keep the air balloon in the target zone for at least 5s
        band_top = target.center_y - TARGET_BAND_HEIGHT // 2
        band_bottom = target.center_y + TARGET_BAND_HEIGHT // 2
        # counter_score to count the seconds inside the target band
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


        balloon.update(hand_input.CURRENT_HAND_STATE)   # mediapipe input
        target.update(dt)

        target.draw(game_surface)
        balloon.draw(game_surface)

        # score display
        score_text = font.render(f"Score: {score}", True, (50, 50, 80))
        game_surface.blit(score_text, (20, 20))

        pygame.display.update()

        # --- Event handler ---
        for event in pygame.event.get():
            # to close pygame windows
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.WINDOWCLOSE:
                running = False

            # to trigger a fainting simulation. In real case scenario we would have the alarm to physicians
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    fainting_simulation.simulation_fainting(True, game_surface, clock, arduino)
                    arduino = arduino_disconnect(arduino)
                    running = False

        # Automatically stop the game after 10 AMT repetitions (i.e. 10s*10=100s)
        if pygame.time.get_ticks() - game_start_time > GAME_DURATION:
            running = False

    # --- Close everything smoothly ---
    # kill thread
    hand_input.STOP_HAND_THREAD.set()
    hand_thread.join(timeout=2)

    cam_win.destroy()
    pygame.quit()
    sys.exit()
