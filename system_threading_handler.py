import threading
from enum import Enum

class SystemState(Enum):
    MONITORING = 0
    GAME = 1
    EXIT = 2

system_state = SystemState.MONITORING
state_lock = threading.Lock()
