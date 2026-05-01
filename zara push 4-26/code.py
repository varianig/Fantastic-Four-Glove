import analogio
import board
import digitalio
from glove import Glove
import time

FORCE_INDEX  = digitalio.DigitalInOut(board.GP16)
FORCE_INDEX.direction = digitalio.Direction.INPUT
FORCE_INDEX.pull = digitalio.Pull.DOWN
 
FORCE_MIDDLE = digitalio.DigitalInOut(board.GP17)
FORCE_MIDDLE.direction = digitalio.Direction.INPUT
FORCE_MIDDLE.pull = digitalio.Pull.DOWN

FORCE_THUMB  = digitalio.DigitalInOut(board.GP18)
FORCE_THUMB.direction = digitalio.Direction.INPUT
FORCE_THUMB.pull = digitalio.Pull.DOWN

FORCE_RING   = digitalio.DigitalInOut(board.GP19)
FORCE_RING.direction = digitalio.Direction.INPUT
FORCE_RING.pull = digitalio.Pull.DOWN
                            
FLEX_INDEX  = analogio.AnalogIn(board.GP26)
FLEX_MIDDLE = analogio.AnalogIn(board.GP27)
FLEX_THUMB  = analogio.AnalogIn(board.GP28)
            
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
time.sleep(1)

# Main Loop
def normalize(val, base, max_val=600):
    # scale 0.0-1.0
    delta = val - base
    return max(0, min(1, delta / (max_val - base)))




print("Main Loop")
threshold = 1.5
prev_mot = set()
mot = set()
action = False
cooldown = False
while True:
    vals = glove.readVals()
    vals_norm = {}
    for val, i in vals.items():
        vals_norm[val] = normalize(i, thresh[val], 650)
        
    line = (
        f"FLEX | I:{vals['FLEX_INDEX']}, {vals_norm['FLEX_INDEX']:4} M:{vals['FLEX_MIDDLE']}, {vals_norm['FLEX_MIDDLE']:4} T:{vals['FLEX_THUMB']}, {vals_norm['FLEX_THUMB']:4}   "
        f"FORCE | I:{vals['FORCE_INDEX']}, {vals_norm['FORCE_INDEX']:3} M:{vals['FORCE_MIDDLE']}, {vals_norm['FORCE_MIDDLE']:3} T:{vals['FORCE_THUMB']}, {vals_norm['FORCE_THUMB']:3} R:{vals['FORCE_RING']}, {vals_norm['FORCE_RING']:3}"
        )
    print(line, end="\r")
    print("\033[F\033[K")
    #print(f"T:{vals['FORCE_THUMB']}, {vals_norm['FORCE_THUMB']}")

    # --- NEW: continuous input tracking ---
    current_mot = set()

    for val, i in vals.items():
        if val in flex and vals_norm[val] > .75:
            current_mot.add(val)
        if val in force and i != 0:
            current_mot.add(val)

    # handle continuous keys
    glove.handleContinuous(current_mot)
    
    pressed = current_mot - prev_mot
    # handle toggle on PRESS only
    if "FORCE_RING" in pressed:
        glove.toggleCursor()
        
    prev_mot = current_mot.copy()
    
    if action == False:
        for val, i in vals.items():
            if val in flex and vals_norm[val] > .4: 
                action = True
            if val in force and i != 0: 
                action = True

    if action == True:
        if glove.getSetting() == 'default':
            for val, i in vals.items():
                if val in flex and vals_norm[val] > .75:
                    mot.add(val)
                if val in force and i != 0:
                    mot.add(val)
            if all(value < thresh[key] + 100 for key, value in vals.items()):
                glove.completeAction(mot)
                action = False
                mot = set()
                cooldown = True
                cooldown_start = time.time()
        else:
            for val, i in vals.items():
                if val in flex and i > thresh[val] * threshold:
                    mot.add(val)
                if val in force and i != 0:
                    mot.add(val)
                
                glove.completeAction(mot)
                action = False
                mot = set()
                cooldown = True
                cooldown_start = time.time()
            

    if cooldown and time.time() - cooldown_start > 0.5:
        cooldown = False
    if cooldown:
        time.sleep(0.05)
        continue
        
    time.sleep(0.01)
    
