![alt text](https://github.com/Allelallecialle/HemoSense/blob/main/images/Demo_hand_detection_open.png?raw=true)

# HemoSense
Hemosense is a **multimodal**, **autonomous** and **adaptive** system to prevent and mitigate adverse events (e.g. vasovagal syncopes) during plasmapheresis and
whole blood donations. The goals are to:
- Improve physical and mental well-being of donors
- Attract new donors
- Improve retention
- Lower workload for physicians

## Functionalities
The functionalities can be divided in 3 main categories: **passive** and **active** interaction, and **environmental** data integration.


The environmental integration is done to set dynamic and personalized risk thresholds. The considered data are the weather info (temperature and humidity), 
donor's profile (gander, age, number of previous donations, etc), and the pre-donation medical assessment (donor anxiety, low blood pressure, etc).


The system passively detect and analyses pallor changes, facial expressions, and gesture to recognize donor's anxiety, physical or emotional distress. These were implemented with the ML algorithms in the reference papers.


The donor actively interacts with the system through a minigame, which goal is to make them correctly perform AMT (applied muscle tension) at the trigger of a low risk threshold for AE.
It is coded in PyGame and the inputs are given with MediaPipe detecting the hand movements.

## What does this repo do?
There are 3 main sections implemented in this demo: the first two are powered by MediaPipe, integrated with OpenCV and PyGame, 
the last one is supported by an Arduino device that communicates with the python code through the serial port. 
Hemosense starts with the facial and fidgeting analysis through the webcam, computing the fainting risk.
Then, the minigame with hand input is triggered by the low risk threshold or by pressing `f`. The last part, simulating the donor's fainting, 
can be triggered by pressing `space bar` and sends an alarm signal to the Arduino device. The code can be quit with `q`.

![alt text](https://github.com/Allelallecialle/HemoSense/blob/main/images/Demo_hand_detection_closed.png?raw=true)
![alt text](https://github.com/Allelallecialle/HemoSense/blob/main/images/arduino_device.png?raw=true)
## Configure and run the project
- Create the virtualenv:
`python3 -m venv .venv`

- Activate it:
`source .venv/bin/activate`

- Install the requisites: `pip install -r requirements.txt`

- Set the interpreter

- Run the `main.py`

## Author
**Alessandra Benassi** - DISI, University of Trento