import sys
import threading
import videogame
from fainting_risk import FaintingRisk
from distress_detection import distress_worker


shared = FaintingRisk()

t = threading.Thread(target=distress_worker, args=(shared,), daemon=True)
t.start()

while not shared.quit:
    if shared.start_game:
        videogame.run_videogame()
        shared.start_game = False

shared.quit = True
t.join()
sys.exit()




