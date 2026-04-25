from glove import Glove
import time

# Setup.        FIX PINS
FORCE_INDEX = analogio.AnalogIn(board.GP26)
FORCE_MIDDLE = analogio.AnalogIn(board.GP26)
FORCE_THUMB = analogio.AnalogIn(board.GP26)
FLEX_INDEX = analogio.AnalogIn(board.GP26)
FLEX_MIDDLE = analogio.AnalogIn(board.GP26)
FLEX_THUMB = analogio.AnalogIn(board.GP26)
FORCE_RING = analogio.AnalogIn(board.GP26)
force = ["FORCE_INDEX", "FORCE_MIDDLE", "FORCE_THUMB", "FORCE_RING"]
flex = ["FLEX_INDEX", "FLEX_MIDDLE", "FLEX_THUMB"]

glove = Glove(FORCE_INDEX, FORCE_MIDDLE, FORCE_THUMB, FLEX_INDEX, FLEX_MIDDLE, FLEX_THUMB, FORCE_RING)

# Calibration
print("Calibrating...")
# Glove.calibrate() returns dict of thresholds, order is forceI, forceM, forceP, flecI, flexM, flexP, forceA
thresh = glove.calibrate()
print("Calibration Complete.\nData:")
print("foI", thresh["FORCE_INDEX"], "\nfoM", thresh["FORCE_MIDDLE"], "\nfoP", thresh["FORCE_THUMB"],
       "\nflI", thresh["FLEX_INDEX"], "\nflM", thresh["FLEX_MIDDLE"], "\nflP", thresh["FLEX_THUMB"], 
       "\nfoA", thresh["FORCE_RING"])
time.sleep(5)

# Main Loop
mot = set()
action = False
while True:
    vals = glove.readVals()
    if action == False:
        for val, i in vals.items():
            if val in flex and i < thresh[val] + 100: 
                action = True
            if val in force and i < thresh[val] + 50: 
                action = True

    if action == True:
        for val, i in vals.items():
            if val in flex and i < thresh[val] + 250:
                if val not in mot:
                    mot.add(val)
            if val in force and i < thresh[val] + 150:
                if val not in mot:
                    mot.add(val)
        if all(value < thresh[key] + 100 for key, value in vals.items()):
            glove.completeAction(mot)
            action = False
            mot = []
            time.sleep(0.3)
        
    time.sleep(0.05)
        
