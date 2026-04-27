from motions import motions, motions_cursor
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import time

class Glove:
    def __init__(self, FORCE_I, FORCE_M, FORCE_P, FLEX_I, FLEX_M, FLEX_P, FORCE_A):
        self.FORCE_I = FORCE_I
        self.FORCE_M = FORCE_M
        self.FORCE_P = FORCE_P
        self.FLEX_I = FLEX_I
        self.FLEX_M = FLEX_M
        self.FLEX_P = FLEX_P
        self.FORCE_A = FORCE_A
        
        self.mouse = Mouse(usb_hid.devices)
        self.kbd = Keyboard(usb_hid.devices)
        self.setting = 'default'

        self.force_i_reading = 0
        self.force_m_reading = 0
        self.force_p_reading = 0
        self.flex_i_reading = 0
        self.flex_m_reading = 0
        self.flex_p_reading = 0
        self.force_a_reading = 0

        self.motions = motions
        self.motions_cursor = motions_cursor
    def readVals(self):
        self.FORCE_INDEX  = 300 if self.FORCE_I.value else 0
        self.FORCE_MIDDLE = 300 if self.FORCE_M.value else 0
        self.FORCE_THUMB  = 300 if self.FORCE_P.value else 0
        self.FORCE_RING   = 300 if self.FORCE_A.value else 0

        self.FLEX_INDEX  = int(self.FLEX_I.value / 200)
        self.FLEX_MIDDLE = int(self.FLEX_M.value / 200)
        self.FLEX_THUMB  = int(self.FLEX_P.value / 200)

        vals = {
            "FORCE_INDEX":  self.FORCE_INDEX,
            "FORCE_MIDDLE": self.FORCE_MIDDLE,
            "FORCE_THUMB":  self.FORCE_THUMB,
            "FLEX_INDEX":   self.FLEX_INDEX,
            "FLEX_MIDDLE":  self.FLEX_MIDDLE,
            "FLEX_THUMB":   self.FLEX_THUMB,
            "FORCE_RING":   self.FORCE_RING
        }
        return vals

    def calibrate(self):
        flex_i_cal = []
        flex_m_cal = []
        flex_p_cal = []

        for i in range(100):
            self.readVals()
            flex_i_cal.append(self.FLEX_INDEX)
            flex_m_cal.append(self.FLEX_MIDDLE)
            flex_p_cal.append(self.FLEX_THUMB)
            time.sleep(0.05)

        thresh = {
            "FORCE_INDEX":  0,
            "FORCE_MIDDLE": 0,
            "FORCE_THUMB":  0,
            "FORCE_RING":   0,
            "FLEX_INDEX":   max(flex_i_cal) + 10,
            "FLEX_MIDDLE":  max(flex_m_cal) + 10,
            "FLEX_THUMB":   max(flex_p_cal) + 10,
        }
        return thresh
    
    def completeAction(self, mot):
        motion_set = self.motions if self.setting == "default" else self.motions_cursor
        for m, i in motion_set.items():
            if set(i) == mot:
                action = m
                break
        if action == False:
            return
                
        if action == 'left click':
            self.leftClick()
        if action == 'right click':
            self.rightClick()
        if action == 'tab':
            self.tab()
        if action == 'shift + tab':
            self.shiftTab()
        if action == 'enter':
            self.enter()
        if action == 'esc':
            self.esc()
        if action == 'pg dwn':
            self.pgDwn()
        if action == 'pg up':
            self.pgUp()
        if action == 'left arrow':
            self.leftArrow()
        if action == 'right arrow':
            self.rightArrow()

        if action == 'toggle cursor':
            self.toggleCursor()
        if action == 'toggle keyboard':
            self.toggleKeyboard()

        if action == 'mouse yneg':
            self.yNeg()
        if action == 'mouse ypos':
            self.yPos()
        if action == 'mouse xneg':
            self.xNeg()
        if action == 'mouse xpos':
            self.xPos()

        if action == 'mouse xneg yneg':
            self.xNeg_yNeg()
        if action == 'mouse xneg ypos':
            self.xNeg_yPos()
        if action == 'mouse xpos yneg':
            self.xPos_yNeg()
        if action == 'mouse xpos ypos':
            self.xPos_yPos()

    def leftClick(self):
        self.mouse.click(Mouse.LEFT_BUTTON)
        time.sleep(0.3)  # debounce
    def rightClick(self):
        self.mouse.click(Mouse.RIGHT_BUTTON)
        time.sleep(0.3)  # debounce
    def tab(self):
        self.kbd.send(Keycode.TAB)
        time.sleep(0.3)  # debounce
    def enter(self):
        self.kbd.send(Keycode.ENTER)
        time.sleep(0.3)  # debounce
    def esc(self):
        self.kbd.send(Keycode.ESCAPE)
        time.sleep(0.3)  # debounce
    def pgDwn(self):
        self.kbd.send(Keycode.DOWN_ARROW)
        time.sleep(0.3)  # debounce
    def pgUp(self):
        self.kbd.send(Keycode.UP_ARROW)
        time.sleep(0.3)  # debounce
    def leftArrow(self):
        self.kbd.send(Keycode.LEFT_ARROW)
        time.sleep(0.3)  # debounce
    def rightArrow(self):
        self.kbd.send(Keycode.RIGHT_ARROW)
        time.sleep(0.3)  # debounce

    def toggleCursor(self):
        if self.setting == "default":
            self.setting = "cursor"
        else:
            self.setting = "default"
    def toggleKeyboard(self):
        self.kbd.send(Keycode.CONTROL, Keycode.WINDOWS, Keycode.O)
        time.sleep(0.3)  # debounce


    def yNeg(self):
        self.mouse.move(0, -100, 0)
        time.sleep(0.3)  # debounce
    def yPos(self):
        self.mouse.move(0, 100, 0)
        time.sleep(0.3)  # debounce
    def xNeg(self):
        self.mouse.move(-100, 0, 0)
        time.sleep(0.3)  # debounce
    def xPos(self):
        self.mouse.move(100, 0, 0)
        time.sleep(0.3)  # debounce

    def xNeg_yNeg(self):
        self.mouse.move(-100, -100, 0)
        time.sleep(0.3)  # debounce
    def xNeg_yPos(self):
        self.mouse.move(-100, 100, 0)
        time.sleep(0.3)  # debounce
    def xPos_yNeg(self):
        self.mouse.move(100, -100, 0)
        time.sleep(0.3)  # debounce
    def xPos_yPos(self):
        self.mouse.move(100, 100, 0)
        time.sleep(0.3)  # debounce
        