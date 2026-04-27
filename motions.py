# "FLEX_INDEX", "FLEX_MIDDLE"

motions = {
    "left click": ["FORCE_THUMB"],
    "right click": ["FLEX_THUMB"],
    "tab": ["FORCE_INDEX"],
    "shift + tab": ["FORCE_MIDDLE"],
    "enter": ["FORCE_MIDDLE", "FORCE_THUMB"],
    "esc": ["FORCE_INDEX", "FORCE_THUMB"],
    "pg dwn": ["FLEX_INDEX"],
    "pg up": ["FLEX_MIDDLE"],
    "left arrow": ["FLEX_INDEX", "FLEX_THUMB"],
    "right arrow": ["FLEX_MIDDLE", "FLEX_THUMB"],

    "toggle cursor": ["FORCE_RING"],
    "toggle keyboard": ["FORCE_INDEX", "FORCE_MIDDLE"] # WIN + CMD + O on windows
}

motions_cursor = {
    "left click": ["FORCE_THUMB"],
    "right click": ["FLEX_THUMB"],

    "mouse yneg": ["FORCE_INDEX"],
    "mouse ypos": ["FLEX_INDEX"],
    "mouse xneg": ["FORCE_MIDDLE"],
    "mouse xpos": ["FLEX_MIDDLE"],

    "mouse xneg yneg": ["FORCE_INDEX", "FORCE_MIDDLE"],
    "mouse xneg ypos": ["FLEX_INDEX", "FORCE_MIDDLE"],
    "mouse xpos yneg": ["FORCE_INDEX", "FLEX_MIDDLE"],
    "mouse xpos ypos": ["FLEX_INDEX", "FLEX_MIDDLE"],

    "toggle cursor": ["FORCE_RING"],
    "toggle keyboard": ["FORCE_INDEX", "FORCE_MIDDLE"] # WIN + CMD + O on windows
}
