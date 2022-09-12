# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_displayio_flipclock.flip_clock`
================================================================================

DisplayIO widget that shows two sets of two digit pairs. It supports "flip clock"
style animations when changing to different values.


* Author(s): Tim Cocks

Implementation Notes
--------------------

**Hardware:**

* `ESP32-S2 Feather TFT <https://www.adafruit.com/product/5300>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""
try:
    from typing import Optional
    from displayio import Bitmap
except ImportError:
    pass

from adafruit_displayio_layout.widgets.widget import Widget
from displayio import Palette  # pylint: disable=ungrouped-imports
from vectorio import Circle
from adafruit_displayio_flipclock.flip_digit import FlipDigit

# Gap in pixels that the colon will be shown in between the two pairs
COLON_SPACE = 12


class FlipClock(Widget):
    """A FlipClock displayio widget that shows two pairs of digits and uses
    flip clock style animations to change between them.

    :param Bitmap static_spritesheet: Spritesheet image of static numbers sprites.
    :param Palette static_spritesheet_palette: Palette to use with the static sprite sheet.
      set all desired transparent or opaque indexes before initializing.
    :param Bitmap top_anim_spritesheet: Spritesheet image of top half animation sprites.
    :param Palette top_anim_palette: Palette to use with the top half animation sprites.
      set all desired transparent or opaque indexes before initializing.
    :param Bitmap bottom_anim_spritesheet: Spritesheet image of bottom half animation sprites.
    :param Palette bottom_anim_palette: Palette to use with the bottom half animation sprites.
      set all desired transparent or opaque indexes before initializing.

    :param int tile_width: Width in pixels of the animation sprite tiles.
    :param int tile_height: Height in pixels of the animation sprite tiles. NOTE: this value
      should be 1/2 the height of the full static digit sprite. Animations cover top and bottom half
      respectively.
    :param int anim_frame_count: The number of frames in the flip animations. Default value is 10
      which is the number contained in the example spritesheets.
    :param float anim_delay: Time in seconds to wait between animation frames.
      Default value is 0.02 seconds
    :param int colon_color: Hex color value to draw the colon between pairs of digits.
      Default is white 0xffffff.
    :param bool dynamic_fading: Whether to use PaleteFadder to dynamically adjust brightness.
    :param float brighter_lebel: Brightness modifier value to use for the brightest portion
      of the aniatmions. Valid range is 0.0 - 1.0.
    :param float medium_level: Brightness modifier value to use for the standard
      portion of the aniatmions. Valid range is 0.0 - 1.0.
    :param float darker_level: Brightness modifier value to use for the darkest "shadow" portion
      of the aniatmions. Valid range is 0.0 - 1.0.
    """

    # pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-locals

    def __init__(
        self,
        static_spritesheet: Bitmap,
        static_spritesheet_palette: Palette,
        top_anim_spritesheet: Bitmap,
        top_anim_palette: Palette,
        bottom_anim_spritesheet: Bitmap,
        bottom_anim_palette: Palette,
        tile_width: int,
        tile_height: int,
        anim_frame_count: int = 10,
        anim_delay: float = 0.02,
        colon_color: int = 0xFFFFFF,
        dynamic_fading: bool = False,
        brighter_level: float = 0.85,
        darker_level: float = 0.6,
        medium_level: float = 0.8,
    ) -> None:

        # initialize parent Widget object
        super().__init__(
            width=tile_width * 4 + COLON_SPACE,
            height=tile_height * 2,
        )

        # store assets and configuration values on self variables to access in other class functions
        self.static_spritesheet = static_spritesheet
        self.static_spritesheet_palette = static_spritesheet_palette
        self.top_anim_spritesheet = top_anim_spritesheet
        self.top_anim_palette = top_anim_palette
        self.bottom_anim_spritesheet = bottom_anim_spritesheet
        self.bottom_anim_palette = bottom_anim_palette
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.anim_frame_count = anim_frame_count
        self.anim_delay = anim_delay
        self.brighter_level = brighter_level
        self.darker_level = darker_level
        self.medium_level = medium_level

        # Create first digit of first pair
        self.digit_0 = FlipDigit(
            self.static_spritesheet,
            self.static_spritesheet_palette,
            self.top_anim_spritesheet,
            self.top_anim_palette,
            self.bottom_anim_spritesheet,
            self.bottom_anim_palette,
            self.tile_width,
            self.tile_height,
            anim_delay=self.anim_delay,
            dynamic_fading=dynamic_fading,
            brighter_level=self.brighter_level,
            darker_level=self.darker_level,
            medium_level=self.medium_level,
        )
        self.digit_0.x = 0
        # append it to parent Group
        self.append(self.digit_0)

        # Create second digit of first pair
        self.digit_1 = FlipDigit(
            self.static_spritesheet,
            self.static_spritesheet_palette,
            self.top_anim_spritesheet,
            self.top_anim_palette,
            self.bottom_anim_spritesheet,
            self.bottom_anim_palette,
            self.tile_width,
            self.tile_height,
            anim_delay=self.anim_delay,
            dynamic_fading=dynamic_fading,
            brighter_level=self.brighter_level,
            darker_level=self.darker_level,
            medium_level=self.medium_level,
        )
        self.digit_1.x = self.tile_width
        # append it to parent Group
        self.append(self.digit_1)

        # Create first digit of second pair
        self.digit_2 = FlipDigit(
            self.static_spritesheet,
            self.static_spritesheet_palette,
            self.top_anim_spritesheet,
            self.top_anim_palette,
            self.bottom_anim_spritesheet,
            self.bottom_anim_palette,
            self.tile_width,
            self.tile_height,
            anim_delay=self.anim_delay,
            dynamic_fading=dynamic_fading,
            brighter_level=self.brighter_level,
            darker_level=self.darker_level,
            medium_level=self.medium_level,
        )

        self.digit_2.x = (self.tile_width) * 2 + COLON_SPACE
        # append it to parent Group
        self.append(self.digit_2)

        # Create second digit of second pair
        self.digit_3 = FlipDigit(
            self.static_spritesheet,
            self.static_spritesheet_palette,
            self.top_anim_spritesheet,
            self.top_anim_palette,
            self.bottom_anim_spritesheet,
            self.bottom_anim_palette,
            self.tile_width,
            self.tile_height,
            anim_delay=self.anim_delay,
            dynamic_fading=dynamic_fading,
            brighter_level=self.brighter_level,
            darker_level=self.darker_level,
            medium_level=self.medium_level,
        )

        self.digit_3.x = self.digit_2.x + self.tile_width
        # append it to parent Group
        self.append(self.digit_3)

        # set colon color
        colon_palette = Palette(1)
        colon_palette[0] = colon_color

        # calculate colon position
        colon_x = self.digit_1.x + self.tile_width + 6
        top_dot_y = self.tile_height * 2 // 3
        bottom_dot_y = (self.tile_height * 2 // 3) * 2

        # create circles for colon
        top_circle = Circle(
            pixel_shader=colon_palette, radius=4, x=colon_x, y=top_dot_y
        )
        bottom_circle = Circle(
            pixel_shader=colon_palette, radius=4, x=colon_x, y=bottom_dot_y
        )

        # add the colon circles to parent Group
        self.append(top_circle)
        self.append(bottom_circle)

    @staticmethod
    def _validate_new_pair(new_pair: str) -> Optional[str]:
        """
        Check if a new value for pair of digits is valid.
        Validates type and length of the value.

        If the value is valid it will be returned, with a leading zero padded
        if necessary.

        :param str new_pair: The new value to validate
        """

        # validate type and length
        if not isinstance(new_pair, str) or not len(new_pair) in (1, 2):
            raise ValueError("Pair Value must be str with length 2")

        # if the new value is length 1
        if len(new_pair) == 1:
            # single zero pad on the left
            new_pair = f"0{new_pair}"

        return new_pair

    @property
    def first_pair(self) -> str:
        """
        The current value of the first pair of digits.
        """
        return f"{str(self.digit_0.value)}{str(self.digit_1.value)}"

    @first_pair.setter
    def first_pair(self, new_pair: str) -> None:
        # validate the new value
        new_pair = self._validate_new_pair(new_pair)

        # if first digit is different
        if self.digit_0.value != int(new_pair[0]):
            # update first digit
            self.digit_0.value = int(new_pair[0])

        # if second digit is different
        if self.digit_1.value != int(new_pair[1]):
            # update second digit
            self.digit_1.value = int(new_pair[1])

    @property
    def second_pair(self) -> str:
        """
        The current value of the second pair of digits.
        """
        return f"{str(self.digit_2.value)}{str(self.digit_3.value)}"

    @second_pair.setter
    def second_pair(self, new_pair: str) -> None:
        # validate new value
        new_pair = self._validate_new_pair(new_pair)

        # if first digit is different
        if self.digit_2.value != int(new_pair[0]):
            # update the first digit
            self.digit_2.value = int(new_pair[0])

        # if the second digit is different
        if self.digit_3.value != int(new_pair[1]):
            # update second digit
            self.digit_3.value = int(new_pair[1])
