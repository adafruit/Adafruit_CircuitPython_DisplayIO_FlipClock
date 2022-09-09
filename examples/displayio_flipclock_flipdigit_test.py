# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
from displayio import Group
import board
from adafruit_displayio_flipclock.flip_digit import FlipDigit
import adafruit_imageload

ANIMATION_DELAY = 0.02
TRANSPARENT_INDEXES = range(11)
BRIGHTER_LEVEL = 0.99
DARKER_LEVEL = 0.5
MEDIUM_LEVEL = 0.9

display = board.DISPLAY
main_group = Group()

static_spritesheet, static_palette = adafruit_imageload.load("static_sheet.bmp")
static_palette.make_transparent(0)

top_animation_spritesheet, top_animation_palette = adafruit_imageload.load("grey_top_animation_sheet.bmp")
bottom_animation_spritesheet, bottom_animation_palette = adafruit_imageload.load("grey_bottom_animation_sheet.bmp")

SPRITE_WIDTH = static_spritesheet.width // 3
SPRITE_HEIGHT = (static_spritesheet.height // 4) // 2

flip_digit = FlipDigit(
    static_spritesheet, static_palette,
    top_animation_spritesheet, top_animation_palette,
    bottom_animation_spritesheet, bottom_animation_palette,
    SPRITE_WIDTH, SPRITE_HEIGHT, anim_delay=ANIMATION_DELAY, transparent_indexes=TRANSPARENT_INDEXES,
    brighter_level=BRIGHTER_LEVEL, darker_level=DARKER_LEVEL, medium_level=MEDIUM_LEVEL
)

flip_digit.anchor_point = (0.5, 0.5)
flip_digit.anchored_position = (display.width // 2, display.height // 2)

main_group.append(flip_digit)
display.show(main_group)

while True:
    for i in range(10):
        flip_digit.value = i

        time.sleep(.75)
