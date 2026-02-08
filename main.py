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
    #shared.start_game = False

elif sth.system_state == sth.SystemState.EXIT:
    #shared.quit = True
    sys.exit(0)

# while not shared.quit:
#     if shared.start_game:
#         videogame.run_videogame()
#         shared.start_game = False

# shared.quit = True
# t.join()
# sys.exit()




