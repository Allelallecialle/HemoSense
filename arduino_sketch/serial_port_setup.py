import time
import serial


def arduino_connection():
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)  # wait for Arduino reset
        print("Arduino connected")
    except serial.SerialException as e:
        print("Arduino not connected:", e)
        arduino = None

    return arduino

def arduino_disconnect(arduino):
    if arduino is not None and arduino.is_open:
        arduino.close()
        print("Arduino disconnected")
    else:
        print("Arduino disconnection failed")

    return