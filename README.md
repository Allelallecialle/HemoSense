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
## Configure and run the project
- Create the virtualenv:
`python3 -m venv .venv`

- Activate it:
`source .venv/bin/activate`

- Install the requisites: `pip install -r requirements.txt`

- Set the interpreter

## Author
**Alessandra Benassi** - DISI, University of Trento