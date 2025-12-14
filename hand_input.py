import pygame
import game_config
import mediapipe

# ============================================
# MEDIA PIPE INPUT (placeholder)
# Replace this with detection
# ============================================

def get_hand_state():
    """
    Placeholder function.
    Replace with MediaPipe detection:
    return "squeeze" or "release"
    """
    # Temporary keyboard mapping for testing:
    # SPACE = squeeze
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        return "squeeze"
    return "release"
