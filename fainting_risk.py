import threading
import numpy as np


class FaintingRisk:
    def __init__(self):
        self.lock = threading.Lock()
        self.fidget = 0.0
        self.stress = 0.0
        self.risk = 0.0
        self.quit = False
        self.start_game = False  # videogame phase enabler
        self.game_running = False

    def update(self, fidget, stress):
        with self.lock:
            self.fidget = fidget
            self.stress = stress

    def get(self):
        with self.lock:
            return self.fidget, self.stress, self.risk, self.start_game

    def risk_computation(self):
        # compute fainting risk combining fidgeting and stress scores. A sigmoid was chosen: value in [0,1],
        # used in DL/ML, smoother function to avoid sudden transitions (=triggers).
        # NOTE: this is a DEMO. In the complete system, there would be a more complex, ML driven computation
        # combining also pallor analysis, weather data, donor's profile and data from the medical assessment
        # Hypothesis for complete implementation: The center of the sigmoid could be fixed at the "donor's base risk",
        # computed by the data previously mentioned, while the real-time risk is computed using the current implementation
        # with also pallor analysis.
        risk = 1 / (1 + np.exp(-(1 * self.fidget + 1 * self.stress)))
        return risk

    def trigger_low_risk(self):
        if self.risk_computation() >= 0.7:
            print("Low risk triggered!")
            self.start_game = True
            self.game_running = True

    def trigger_high_risk(self):
        if self.risk_computation() >= 0.9:
            print("Donor fainting!")
            print("Send alarm to physician through arduino (not in this demo).")