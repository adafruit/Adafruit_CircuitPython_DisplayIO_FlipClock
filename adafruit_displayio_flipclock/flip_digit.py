# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_displayio_flipclock.flip_digit`
================================================================================

DisplayIO widgets for a single digit that supports "flip clock" style animations
when changing the value showing.


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
    from typing import Optional  # pylint: disable=unused-import
    from displayio import Bitmap
except ImportError:
    pass
import time
from adafruit_displayio_layout.widgets.widget import Widget
from displayio import TileGrid, Palette  # pylint: disable=ungrouped-imports


class FlipDigit(Widget):
    """
    DisplayIO widgets for a single digit that supports "flip clock" style animations
    when changing the value showing. User must load static and animation spritesheets
    and pass them in for initialization.

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
    :param bool dynamic_fading: Whether to use PaleteFadder to dynamically adjust brightness.
    :param float brighter_level: Brightness modifier value to use for the brightest
      portion of the animations. Valid range is 0.0 - 1.0.
    :param float medium_level: Brightness modifier value to use for the standard
      portion of the animations. And the static digit sprites. Valid range is 0.0 - 1.0.
    :param float darker_level: Brightness modifier value to use for the
      darkest "shadow" portion of the animations. Valid range is 0.0 - 1.0.
    """

    # pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-locals

    # all characters that are valid
    VALID_CHARACTERS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9)

    # map of sprite indexes for top half animation sprite sheet
    TOP_HALF_SPRITE_INDEX_MAP = {
        0: 0,
        1: 1,
        2: 2,
        3: 6,
        4: 7,
        5: 8,
        6: 12,
        7: 13,
        8: 14,
        9: 18,
    }
    # map of sprite indexes for bottom half animation sprite sheet
    BOTTOM_HALF_SPRITE_INDEX_MAP = {
        0: 3,
        1: 4,
        2: 5,
        3: 9,
        4: 10,
        5: 11,
        6: 15,
        7: 16,
        8: 17,
        9: 21,
    }

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
        dynamic_fading: bool = True,
        brighter_level: float = 0.85,
        darker_level: float = 0.6,
        medium_level: float = 0.8,
    ) -> None:
        # initialize parent Widget object
        super().__init__(width=tile_width, height=tile_height * 2)

        # setup for dynamic fading (or not if it's disabled)
        self.dynamic_fading = dynamic_fading
        static_palette = None
        bottom_palette = None
        top_palette = None
        if dynamic_fading:
            # pylint: disable=import-outside-toplevel
            from cedargrove_palettefader import (
                PaletteFader,
            )

            self.static_fader = PaletteFader(
                static_spritesheet_palette, medium_level, 1.0
            )
            self.darker_static_fader = PaletteFader(
                static_spritesheet_palette, darker_level, 1.0
            )
            self.bottom_anim_fader = PaletteFader(
                bottom_anim_palette, brighter_level, 1.0
            )
            self.top_anim_fader = PaletteFader(top_anim_palette, darker_level, 1.0)
            static_palette = self.static_fader.palette
            bottom_palette = self.bottom_anim_fader.palette
            top_palette = self.top_anim_fader.palette
        else:
            static_palette = static_spritesheet_palette
            bottom_palette = bottom_anim_palette
            top_palette = top_anim_palette

        # store animation variables on self for access in other functions
        self.anim_delay = anim_delay
        self.anim_frame_count = anim_frame_count

        # top static tilegrid init
        self.top_static_tilegrid = TileGrid(
            static_spritesheet,
            pixel_shader=static_palette,
            height=1,
            width=1,
            tile_width=tile_width,
            tile_height=tile_height,
        )

        # bottom static tilegrid init
        self.bottom_static_tilegrid = TileGrid(
            static_spritesheet,
            pixel_shader=static_palette,
            height=1,
            default_tile=3,
            width=1,
            tile_width=tile_width,
            tile_height=tile_height,
        )

        # top animation tilegrid init
        self.top_anim_tilegrid = TileGrid(
            top_anim_spritesheet,
            pixel_shader=top_palette,
            height=1,
            width=1,
            tile_width=tile_width,
            tile_height=tile_height,
        )

        # bottom animation tilegrid init
        self.bottom_anim_tilegrid = TileGrid(
            bottom_anim_spritesheet,
            pixel_shader=bottom_palette,
            height=1,
            width=1,
            tile_width=tile_width,
            tile_height=tile_height,
        )

        # add static tilegrids to parent Group
        self.append(self.top_static_tilegrid)
        self.append(self.bottom_static_tilegrid)

        # set y position of bottom static tilegrid
        self.bottom_static_tilegrid.y = tile_height

        # hide the animation tilegrids
        self.top_anim_tilegrid.hidden = True
        self.bottom_anim_tilegrid.hidden = True

        # add the animation tilegrids to parent Group
        self.append(self.top_anim_tilegrid)
        self.append(self.bottom_anim_tilegrid)

        # set y position of bottom animation tilegrid
        self.bottom_anim_tilegrid.y = tile_height

        # variable to hold current value
        self._value = 0

        # variables used during animation frames
        self.current_animation_frame = 0
        self.top_animating_value = None
        self.bottom_animating_value = None

    @property
    def value(self) -> int:
        """
        The current value of the digit as an integer.
        """
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        """
        Set a new value to show on the flip digit,
        animating as necessary to change to the
        new value.
        """
        # ignore new_value if it's the same as current
        if new_value != self.value:
            # if the new value is valid
            if (
                isinstance(new_value, int)
                and 0 <= new_value <= 9
                and new_value in FlipDigit.VALID_CHARACTERS
            ):
                # store current value to use later
                _old_value = self.value

                # update the value variable
                self._value = new_value

                # set the first frame of the animation spritesheet into
                # top animation tilegrid
                self.top_anim_tilegrid[0] = _old_value * self.anim_frame_count

                # show the top animation tilegrid
                self.top_anim_tilegrid.hidden = False

                # set the top static tilegrid to its new value
                # This is hidden behind the top animation tilegrid initially
                self.top_static_tilegrid[0] = FlipDigit.TOP_HALF_SPRITE_INDEX_MAP[
                    new_value
                ]

                # if dynamic fading is enabled
                if self.dynamic_fading:
                    # set the bottom static tilegrid to use the darker color palette
                    self.bottom_static_tilegrid.pixel_shader = (
                        self.darker_static_fader.palette
                    )

                # Run the top half flip animation
                self.top_flip_animate(value=_old_value)

                # hide the top animation tilegrid
                self.top_anim_tilegrid.hidden = True

                # set the bottom animation tilegrid to it's new value
                self.bottom_anim_tilegrid[0] = new_value * self.anim_frame_count

                # show the bottom animation tilegrid
                self.bottom_anim_tilegrid.hidden = False

                # run the bottom half flip animation
                self.bottom_flip_animate(value=new_value)

                # set the bottom static tilegrid to new value sprite index
                self.bottom_static_tilegrid[0] = FlipDigit.BOTTOM_HALF_SPRITE_INDEX_MAP[
                    new_value
                ]

                # hide the bottom animation tilegrid
                # which reveals the bottom static tilegrid
                self.bottom_anim_tilegrid.hidden = True

                # if dynamic faiding is enabled
                if self.dynamic_fading:
                    # set the bottom static tilegrid back to the medium brightness palette
                    self.bottom_static_tilegrid.pixel_shader = self.static_fader.palette

            else:  # new_value was invalid
                raise ValueError(
                    f"Invalid new value: {type(new_value)}: {new_value}. Must be int 0-9"
                )

    def top_flip_animate(self, value: int) -> None:
        """
        Blocking function that displays the top animation sprites sequentially
        sleeping for anim_delay between each.
        """
        # loop over frame count
        for i in range(self.anim_frame_count):
            # set the top animation sprite to current animation frame sprite index
            self.top_anim_tilegrid[0] = i + (value * self.anim_frame_count)

            # sleep for delay
            time.sleep(self.anim_delay)

    def bottom_flip_animate(self, value: int) -> None:
        """
        Blocking function that displays the bottom animation sprites sequentially
        sleeping for anim_delay between each.
        """
        # loop over frame count
        for i in range(self.anim_frame_count):
            # set the bottom animation sprite to current animation frame sprite index
            self.bottom_anim_tilegrid[0] = i + (value * self.anim_frame_count)

            # sleep for delay
            time.sleep(self.anim_delay)
