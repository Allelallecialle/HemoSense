import cv2
import pygame
import numpy as np
import game_config
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

CURRENT_HAND_STATE = "release"  # default state

# Create a hand landmarker instance with the live stream mode:
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='/path/to/model.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=1,
    result_callback=print_result)
with HandLandmarker.create_from_options(options) as landmarker:
    pass

def capture_from_webcam():
    # Use OpenCV’s VideoCapture to start capturing from the webcam.
    cam = cv2.VideoCapture(0)
    frame_number = 0

    # Create a loop to read the latest frame from the camera using VideoCapture#read()
    while cam.isOpened():
        ret, frame = cam.read()

        if np.shape(frame) == ():
            cam.release()
            cv2.destroyAllWindows()

        frame_number = frame_number + 1
        # Convert the frame received from OpenCV to a MediaPipe’s Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    cam.release()
    cv2.destroyAllWindows()

def mediapipe_get_hand_state():
    """
    MediaPipe detection of the hand state.
    Returns "squeeze" or "release"
    """
    # Send live image data to perform hand landmarks detection.
    # The results are accessible via the `result_callback` provided in
    # the `HandLandmarkerOptions` object.
    # The hand landmarker must be created with the live stream mode.
    #landmarker.detect_async(mp_image, frame_timestamp_ms)
    # if :
    #     return "squeeze"
    # return "release"

def get_hand_state():
    """
    Test function for the videogame development with keyboard input.
    Returns "squeeze" or "release"
    """
    # Temporary keyboard mapping for testing:
    #SPACE = squeeze
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        return "squeeze"
    return "release"