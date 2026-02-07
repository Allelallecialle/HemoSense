import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_face = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# to compute euclidean distance of landmarks
def euclid(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def distress_worker(shared):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)

    with (mp_face.FaceMesh(
        refine_landmarks=True,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face,
    mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose):

        prev_lh = None
        prev_rh = None
        prev_head = None
        fidget_hist, stress_hist = [], []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_res = face.process(frame_rgb)
            pose_res = pose.process(frame_rgb)

            fidget_score = 0.0
            stress_score = 0.0

            # ---------------- Fidgeting detection from pose ----------------
            if pose_res.pose_landmarks:
                # draw pose landmarks (wrists)
                lm = pose_res.pose_landmarks.landmark
                lh = (lm[mp_pose.PoseLandmark.LEFT_WRIST].x,
                      lm[mp_pose.PoseLandmark.LEFT_WRIST].y)
                rh = (lm[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                      lm[mp_pose.PoseLandmark.RIGHT_WRIST].y)

                #draw landmarks
                lx, ly = int(lh[0] * w), int(lh[1] * h)
                rx, ry = int(rh[0] * w), int(rh[1] * h)
                cv2.circle(frame, (lx, ly), 8, (0, 255, 0), -1)
                cv2.circle(frame, (rx, ry), 8, (0, 255, 0), -1)


                if prev_lh and prev_rh:
                    # compute fidgeting score with wrist movements
                    # sum because one can be occluded or not moving
                    fidget_score = euclid(lh, prev_lh) + euclid(rh, prev_rh)

                prev_lh, prev_rh = lh, rh

            # ---------------- Stress detection from face ----------------
            if face_res.multi_face_landmarks:
                face_lm = face_res.multi_face_landmarks[0]
                lm = face_lm.landmark
                FACE_POINTS = {
                    "eye_top": 159,
                    "eye_bottom": 145,
                    "mouth_top": 13,
                    "mouth_bottom": 14,
                    "head": 1
                }
                # draw face landmarks (only the ones considered, they're a lot so frames slow down)
                for name, idx in FACE_POINTS.items():
                    x = int(lm[idx].x * w)
                    y = int(lm[idx].y * h)
                    cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)
                    cv2.putText(frame, name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

                # defined landmark distances for open eye and mouth, head
                # https://medium.com/@asadullahdal/eyes-https://medium.com/@asadullahdal/eyes-blink-detector-and-counter-mediapipe-a66254eb002cblink-detector-and-counter-mediapipe-a66254eb002c
                eye_open = abs(lm[159].y - lm[145].y)
                mouth_open = abs(lm[13].y - lm[14].y)
                head = (lm[1].x, lm[1].y)

                #compute head movement
                if prev_head:
                    head_jitter = euclid(head, prev_head)
                else:
                    head_jitter = 0
                prev_head = head

                # compute stress score with empirically chosen values
                # (e.g. lower weight for head_jitter because it's normal to move the head)
                # stress score increases with: a lot of blinking, head and mouth movements
                stress_score = (
                    2.5 * eye_open +
                    1.5 * mouth_open +
                    1.0 * head_jitter
                )

            # average the stress and fidget scores (but check if there's enough data, i.e. frames)
            fidget_hist.append(fidget_score)
            stress_hist.append(stress_score)
            if len(fidget_hist) > 15:
                fidget_hist.pop(0)
            if len(stress_hist) > 15:
                stress_hist.pop(0)

            if fidget_hist:
                fidget_avg = np.mean(fidget_hist)
            else:
                fidget_avg = 0

            if stress_hist:
                stress_avg = np.mean(stress_hist)
            else:
                stress_avg = 0

            # ---------------- Final computation ----------------
            # Check FaintingRisk class for the actual computation
            # Risk is set in the interval [0,1] so here pass 1.0 if the value is higher
            shared.update(
                    fidget=min(fidget_avg * 4, 1.0),
                    stress=min(stress_avg * 4, 1.0))
            risk = shared.risk_computation()

            #continuously check the thresholds
            shared.trigger_low_risk()
            shared.trigger_high_risk()

            # show scores on video
            cv2.rectangle(frame, (10, 10), (340, 100), (0, 0, 0), -1)
            cv2.putText(frame, f"Fidget: {shared.fidget:.2f}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.putText(frame, f"Stress: {shared.stress:.2f}", (20, 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.putText(frame, f"Risk:   {risk:.2f}", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,80,255), 2)

            cv2.imshow("Fainting Risk Monitoring", frame)

            # F to trigger low risk fainting and start the AMT videogame; q to quit
            if cv2.waitKey(1) & 0xFF == ord('f'):
                shared.start_game = True
                shared.game_running = True
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                shared.quit = True
                break

            time.sleep(0.04)

    cap.release()
    cv2.destroyAllWindows()

