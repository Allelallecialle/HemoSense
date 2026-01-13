import pygame
from game_config import *

def show_instruction_screen(screen, clock):
    start_time = pygame.time.get_ticks()

    font_title = pygame.font.SysFont("Verdana", 42, bold=True)
    font_text = pygame.font.SysFont("Verdana", 28, bold=True)

    running_intro = True
    while running_intro:
        clock.tick(FPS)
        screen.fill((180, 220, 255))

        title = font_title.render("Balloon Glide Game", True, (50, 70, 120))
        line1 = font_text.render("Open and close your hand to move the balloon", True, (60, 60, 60))
        line2 = font_text.render("Up: squeeze", True, (60, 60, 60))
        line3 = font_text.render("Down: release", True, (60, 60, 60))
        line4 = font_text.render("Keep it inside the blue band to score points", True, (60, 60, 60))

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - title.get_height()//2 - 200))
        screen.blit(line1, (WIDTH//2 - line1.get_width()//2, HEIGHT//2 - line1.get_height()//2))
        screen.blit(line2, (WIDTH//2 - line2.get_width()//2, HEIGHT//2 - line2.get_height()//2 + 100))
        screen.blit(line3, (WIDTH//2 - line3.get_width()//2, HEIGHT//2 - line3.get_height()//2 + 150))
        screen.blit(line4, (WIDTH//2 - line4.get_width()//2, HEIGHT // 2 - line4.get_height()//2 + 250))

        pygame.display.update()

        # Auto start after 5 seconds
        if pygame.time.get_ticks() - start_time > 7000:
            running_intro = False
