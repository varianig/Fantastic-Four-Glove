from motions import motions, motions_cursor
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import time

class Glove:
    def __init__(self):
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

    def readVals(self, FORCE_I, FORCE_M, FORCE_P, FLEX_I, FLEX_M, FLEX_P, FORCE_A):
        self.FORCE_INDEX = int(FORCE_I.value / 200)
        self.FORCE_MIDDLE = int(FORCE_M.value / 200)
        self.FORCE_THUMB = int(FORCE_P.value / 200)
        self.FLEX_INDEX = int(FLEX_I.value / 200)
        self.FLEX_MIDDLE = int(FLEX_M.value / 200)
        self.FLEX_THUMB = int(FLEX_P.value / 200)
        self.FORCE_RING = int(FORCE_A.value / 200)

        vals = {
            "FORCE_INDEX": self.FORCE_INDEX, 
            "FORCE_MIDDLE": self.FORCE_MIDDLE,
            "FORCE_THUMB": self.FORCE_THUMB, 
            "FLEX_INDEX": self.FLEX_INDEX, 
            "FLEX_MIDDLE": self.FLEX_MIDDLE, 
            "FLEX_THUMB": self.FLEX_THUMB, 
            "FORCE_RING": self.FORCE_RING
            }
        return vals

    def calibrate(self):
        force_i_cal = force_m_cal = force_p_cal = flex_i_cal = flex_m_cal = flex_p_cal = force_a_cal = []

        for i in range(100):
            self.readVals()

            force_i_cal.append(self.FORCE_INDEX)
            force_m_cal.append(self.FORCE_MIDDLE)
            force_p_cal.append(self.FORCE_THUMB)
            flex_i_cal.append(self.FLEX_INDEX)
            flex_m_cal.append(self.FLEX_MIDDLE)
            flex_p_cal.append(self.FLEX_THUMB)
            force_a_cal.append(self.FORCE_RING)
            time.sleep(0.05)

        thresh_forceI = max(force_i_cal) + 10
        thresh_forceM = max(force_m_cal) + 10
        thresh_forceP = max(force_p_cal) + 10
        thresh_flexI = max(flex_i_cal) + 10
        thresh_flexM = max(flex_m_cal) + 10
        thresh_flexP = max(flex_p_cal) + 10
        thresh_forceA = max(force_a_cal) + 10
        
        thresh = {
            "FORCE_INDEX": thresh_forceI, 
            "FORCE_MIDDLE": thresh_forceM, 
            "FORCE_THUMB": thresh_forceP, 
            "FLEX_INDEX": thresh_flexI, 
            "FLEX_MIDDLE": thresh_flexM,
            "FLEX_THUMB": thresh_flexP, 
            "FORCE_RING": thresh_forceA
        }
        return thresh

    def completeAction(self, mot):
        mot.sort()
        for m, i in self.motions.items():
            if i == mot:
                action = m
        
        if self.setting == "default":
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

        if self.setting == "cursor":
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

            if action == 'toggle cursor':
                self.toggleCursor()

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
        self.setting = 'cursor'
        time.sleep(0.3)  # debounce
    def toggleKeyboard(self):
        self.kbd.send(Keycode.WINDOWS, Keycode.COMMAND, Keycode.O)
        time.sleep(0.3)  # debounce


    def yNeg(self):
        self.mouse.move(0, -100, 0)
        time.sleep(0.3)  # debounce
    def yPos(self):
        self.mouse.move(0, 100, 0)
        time.sleep(0.3)  # debounce
    def xNeg(self):
        self.mouse.move(100, 0, 0)
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
        