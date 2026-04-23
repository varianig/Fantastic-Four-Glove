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
force = [FORCE_INDEX, FORCE_MIDDLE, FORCE_THUMB, FORCE_RING]
flex = [FLEX_INDEX, FLEX_MIDDLE, FLEX_THUMB]

glove = Glove()

# Calibration
print("Calibrating...")
# Glove.calibrate() returns dict of thresholds, order is forceI, forceM, forceP, flecI, flexM, flexP, forceA
thresh = glove.calibrate()
print("Calibration Complete.\nData:")
print("foI", thresh[0], "\nfoM", thresh[1], "\nfoP", thresh[2], "\nflI", thresh[3], "\nflM", thresh[4], "\nflP", thresh[5], "\nfoA", thresh[6])
time.sleep(5)

# Main Loop
mot = []
action = False
while True:
    vals = glove.readVals(FORCE_INDEX, FORCE_MIDDLE, FORCE_THUMB, FLEX_INDEX, FLEX_MIDDLE, FLEX_THUMB, FORCE_RING)
    if action == False:
        for val, i in vals.items():
            if val in flex and i < thresh[val] + 100: 
                action = True
            if val in force and i < thresh[val] + 50: 
                action = True

    if action == True:
        for val, i in vals.items():
            if val in flex and val < thresh[val] + 250:
                if val not in mot:
                    mot.append(val)
            if val in force and val < thresh[val] + 150:
                if val not in mot:
                    mot.append(val)
        if all(i < thresh[val] + 100 for i, val in vals):
            glove.completeAction(mot)
        
    time.sleep(0.05)
        
