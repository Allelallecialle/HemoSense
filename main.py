import sys
import threading
import videogame
from fainting_risk import FaintingRisk
from distress_detection import distress_worker
import system_threading_handler as sth


shared = FaintingRisk()
print(sth.system_state)

t = threading.Thread(target=distress_worker, args=(shared,))
t.start()
t.join()

# open cam 2 safely, only after webcam thread is killed -> avoids mediapipe-openCV resources lock
if sth.system_state == sth.SystemState.GAME:
    videogame.run_videogame()

elif sth.system_state == sth.SystemState.EXIT:
    sys.exit(0)

