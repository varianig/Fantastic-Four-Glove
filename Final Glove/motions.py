from main import FORCE_INDEX, FORCE_MIDDLE, FORCE_THUMB, FLEX_INDEX, FLEX_MIDDLE, FLEX_THUMB, FORCE_RING

motions = {
    "left click": [FORCE_THUMB],
    "right click": [FLEX_MIDDLE],
    "tab": [FORCE_INDEX],
    "shift + tab": [FORCE_MIDDLE],
    "enter": [FORCE_MIDDLE, FORCE_THUMB],
    "esc": [FORCE_INDEX, FORCE_THUMB],
    "pg dwn": [FLEX_INDEX, FLEX_THUMB],
    "pg up": [FLEX_INDEX],
    "left arrow": [FLEX_INDEX, FLEX_THUMB],
    "right arrow": [FLEX_MIDDLE, FLEX_THUMB],

    "toggle cursor": [FORCE_RING],
    "toggle keyboard": [FLEX_THUMB] # WIN + CMD + O on windows
}

motions_cursor = {
    "mouse yneg": [FORCE_INDEX],
    "mouse ypos": [FORCE_MIDDLE],
    "mouse xneg": [FORCE_THUMB],
    "mouse xpos": [FLEX_THUMB],

    "mouse xneg yneg": [FORCE_INDEX, FORCE_THUMB],
    "mouse xneg ypos": [FORCE_MIDDLE, FORCE_THUMB],
    "mouse xpos yneg": [FLEX_THUMB, FORCE_INDEX],
    "mouse xpos ypos": [FLEX_THUMB, FORCE_MIDDLE],

    "toggle cursor": [FORCE_RING]
}