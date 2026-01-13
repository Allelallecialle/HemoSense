from game_config import *
import pygame

def simulation_fainting(trigger_fainting, screen, clock):
    if trigger_fainting:
        running_fainting = True
        while running_fainting:
            clock.tick(FPS)
            screen.fill((200, 200, 200))

            font = pygame.font.SysFont("Verdana", 40, bold=True)
            msg = font.render("Fainting simulation", True, (120, 0, 0))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(3000)



            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running_fainting = False
                        trigger_fainting = False
