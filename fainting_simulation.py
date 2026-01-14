import sys

from game_config import *
import pygame
import time
import serial
import numpy as np

def simulation_fainting(trigger_fainting, screen, clock, arduino):
    sent = False
    if trigger_fainting:
        running_fainting = True
        while running_fainting:
            clock.tick(FPS)
            screen.fill((200, 200, 200))

            font = pygame.font.SysFont("Verdana", 40, bold=True)
            msg = font.render("Fainting simulation", True, (120, 0, 0))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            #------------
            # sending serial input to arduino

            if not sent:
                if arduino is not None and arduino.is_open:
                    random_num = np.random.randint(1, 20)
                    arduino.write(str(random_num).encode())
                    arduino.flush()
                    print("sent:", random_num)
                    sent = True
            #-----------------------
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        trigger_fainting = False
                        running_fainting = False

                if event.type == pygame.QUIT:
                    trigger_fainting = False
                    running_fainting = False

    return