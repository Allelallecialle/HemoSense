import mediapipe as mp
from mediapipe_utils import *

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# initialize the global var to make it importable to main
CURRENT_HAND_STATE = "release"
LAST_HAND_RESULT = None

def capture_from_camera():
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path='./mediapipe_models/hand_landmarker.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        num_hands=1,
        result_callback=set_hand_state)

    cam = cv2.VideoCapture(2)  # to capture from external camera
    # Use OpenCV’s VideoCapture to start capturing from the webcam.
    #cam = cv2.VideoCapture(0)
    frame_number = 0

    with HandLandmarker.create_from_options(options) as landmarker:
        # loop to read the latest frame from the camera
        while cam.isOpened():
            ret, frame = cam.read()

            if np.shape(frame) == ():
                break

            frame_number += 1
            # convert the opencv frame to a mediapipe Image object
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
                                data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            landmarker.detect_async(mp_image, frame_number)

            # DEBUG
            cv2.putText(frame, CURRENT_HAND_STATE,
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
            annotated_image = frame.copy()
            if LAST_HAND_RESULT is not None:
                annotated_image = draw_landmarks_on_image(
                    cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB),
                    LAST_HAND_RESULT
                )
            cv2.imshow("Hand Detection", cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))


            # exit while
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()
        landmarker.close()

def mediapipe_get_hand_state(landmarks):
    """
    MediaPipe detection of the hand state.
    Returns "squeeze" or "release"
    If the fingertips are close to the palm -> 'squeeze'
    else -> 'release'
    """
    # landmarks numbers we need
    TIP_IDS = [4, 8, 12, 16, 20]  # tips of fingers
    WRIST_ID = 0  # to compute distance from the fingers

    distances = []

    wrist = landmarks[WRIST_ID]
    for tip_id in TIP_IDS:
        tip = landmarks[tip_id]
        dist = np.linalg.norm(
            np.array([tip.x - wrist.x, tip.y - wrist.y])
        )   #compute the norm = the magnitude of distance vector
        distances.append(dist)

    avg_dist = np.mean(distances)   # some fingers may close earlier/later so average the distances

    # threshold chosen empirically
    if avg_dist < 0.2:
        return "squeeze"
    else:
        return "release"

def set_hand_state(landmarks, output_image, timestamp):
    global CURRENT_HAND_STATE   # set to global var to see it from main. More convenient than returning a value
    global LAST_HAND_RESULT

    LAST_HAND_RESULT = landmarks  #store landmarks for visualization

    # Safety check: no hands detected
    if not landmarks.hand_landmarks:
        CURRENT_HAND_STATE = "release"
        return

    try:
        res = landmarks.hand_landmarks[0]
        CURRENT_HAND_STATE = mediapipe_get_hand_state(res)
    except IndexError:
        CURRENT_HAND_STATE = "release"  # default state