#use background image dimensions in pixels
WIDTH = 1724
HEIGHT = 974
FPS = 30

GAME_DURATION = 100000  # 100 s in ms. Time needed for 10 AMT

BALLOON_WIDTH = 80
BALLOON_HEIGHT = 120

BALLOON_START_Y = HEIGHT // 2
BALLOON_X = WIDTH // 5

ASCENT_SPEED = 1.7
GRAVITY = 0.8
DAMPING = 0.75

TARGET_BAND_HEIGHT = 170
TARGET_OSCILLATION_SPEED = 0.5   # speed of movement

TARGET_PERIOD = 7.5          # AMT needs approximately 5s of muscle tension. Set to 7s for reaction time and more relaxed animation
TARGET_AMPLITUDE = 110
