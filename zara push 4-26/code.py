import analogio
import board
import digitalio
from glove import Glove
import time

# set up force sensors as digital inputs with pull-down resistors
FORCE_INDEX  = digitalio.DigitalInOut(board.GP16) #Red
FORCE_INDEX.direction = digitalio.Direction.INPUT
FORCE_INDEX.pull = digitalio.Pull.DOWN
 
FORCE_MIDDLE = digitalio.DigitalInOut(board.GP17) #Yellow
FORCE_MIDDLE.direction = digitalio.Direction.INPUT
FORCE_MIDDLE.pull = digitalio.Pull.DOWN

FORCE_THUMB  = digitalio.DigitalInOut(board.GP18) #Blue
FORCE_THUMB.direction = digitalio.Direction.INPUT
FORCE_THUMB.pull = digitalio.Pull.DOWN

FORCE_RING   = digitalio.DigitalInOut(board.GP19) #Purple
FORCE_RING.direction = digitalio.Direction.INPUT
FORCE_RING.pull = digitalio.Pull.DOWN

# set up flex sensors as analog inputs
FLEX_INDEX  = analogio.AnalogIn(board.GP26) #Brown
FLEX_MIDDLE = analogio.AnalogIn(board.GP27) #Orange
FLEX_THUMB  = analogio.AnalogIn(board.GP28) #Green

# sensor name lists used for type checking later
force = ["FORCE_INDEX", "FORCE_MIDDLE", "FORCE_THUMB", "FORCE_RING"]
flex = ["FLEX_INDEX", "FLEX_MIDDLE", "FLEX_THUMB"]

glove = Glove(FORCE_INDEX, FORCE_MIDDLE, FORCE_THUMB, FLEX_INDEX, FLEX_MIDDLE, FLEX_THUMB, FORCE_RING)

# run calibration while hand is at rest
print("Calibrating...")
# glove.calibrate() returns dict of thresholds, order is forceI, forceM, forceP, flecI, flexM, flexP, forceA
thresh = glove.calibrate()
print("Calibration Complete.\nData:")
print("foI", thresh["FORCE_INDEX"], "\nfoM", thresh["FORCE_MIDDLE"], "\nfoP", thresh["FORCE_THUMB"],
       "\nflI", thresh["FLEX_INDEX"], "\nflM", thresh["FLEX_MIDDLE"], "\nflP", thresh["FLEX_THUMB"], 
       "\nfoA", thresh["FORCE_RING"])
print(thresh)
time.sleep(1)

# normalize a sensor value to 0.0-1.0 relative to its calibrated baseline
def normalize(val, base, max_val=600):
    delta = val - base
    return max(0, min(1, delta / (max_val - base)))


print("Main Loop")
threshold = 1.5
prev_mot = set()   # sensors active on the previous loop iteration
mot = set()        # sensors accumulated during the current gesture
action = False     # true while a gesture is being built
cooldown = False   # true briefly after an action fires to prevent re-triggering

while True:
    vals = glove.readVals()

    # normalize all sensor values against calibrated thresholds
    vals_norm = {}
    for val, i in vals.items():
        vals_norm[val] = normalize(i, thresh[val], 650)

    # debug print for thumb sensors
    print(f"foT:{vals['FORCE_THUMB']}, {vals_norm['FORCE_THUMB']}	flT:{vals['FLEX_THUMB']}, {vals_norm['FLEX_THUMB']}")

    # build the set of sensors currently active above their threshold
    current_mot = set()
    for val, i in vals.items():
        if val in flex and vals_norm[val] > .75:
            current_mot.add(val)
        if val in force and i != 0:
            current_mot.add(val)

    # pass current active sensors to handle held keys like arrow keys
    glove.handleContinuous(current_mot)
    
    # detect newly pressed sensors this frame
    pressed = current_mot - prev_mot
    # toggle cursor mode on the frame ring finger is first pressed
    if "FORCE_RING" in pressed:
        glove.toggleCursor()
        
    prev_mot = current_mot.copy()
    
    # start building a gesture once any sensor crosses its activation threshold
    if action == False:
        for val, i in vals.items():
            if val in flex and vals_norm[val] > .4: 
                action = True
            if val in force and i != 0: 
                action = True

    if action == True:
        if glove.getSetting() == 'default':
            # accumulate active sensors into the gesture set
            for val, i in vals.items():
                if val in flex and vals_norm[val] > .75:
                    mot.add(val)
                if val in force and i != 0:
                    mot.add(val)
            # fire the action once all sensors fall back to near-resting values
            if all(value < thresh[key] + 100 for key, value in vals.items()):
                glove.completeAction(mot)
                action = False
                mot = set()
                cooldown = True
                cooldown_start = time.time()
        else:
            # in cursor mode fire action immediately without waiting for release
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

    # after an action fires wait 0.5 seconds before accepting new gestures
    if cooldown and time.time() - cooldown_start > 0.5:
        cooldown = False
    if cooldown:
        time.sleep(0.05)
        continue
        
    time.sleep(0.01)
