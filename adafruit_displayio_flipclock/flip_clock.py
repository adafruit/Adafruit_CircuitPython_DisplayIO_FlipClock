from adafruit_displayio_layout.widgets.widget import Widget
from displayio import Palette

from flip_digit import FlipDigit
from vectorio import Circle

COLON_SPACE = 12


class FlipClock(Widget):
    def __init__(self, static_spritesheet, static_spritesheet_palette, top_anim_spritesheet,
                 top_anim_palette, bottom_anim_spritesheet, bottom_anim_palette,
                 tile_width, tile_height, anim_frame_count=10, anim_delay=.02, transparent_indexes=[],
                 brighter_level=0.85, darker_level=0.6, medium_level=0.8):
        super().__init__(
            width=tile_width * 4 + COLON_SPACE,
            height=tile_height * 2,
        )

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
        self.transparent_indexes = transparent_indexes
        self.brighter_level = brighter_level
        self.darker_level = darker_level
        self.medium_level = medium_level

        self.digit_0 = FlipDigit(
            self.static_spritesheet, self.static_spritesheet_palette,
            self.top_anim_spritesheet, self.top_anim_palette,
            self.bottom_anim_spritesheet, self.bottom_anim_palette,
            self.tile_width, self.tile_height, anim_delay=self.anim_delay,
            transparent_indexes=self.transparent_indexes,
            brighter_level=self.brighter_level, darker_level=self.darker_level, medium_level=self.medium_level
        )
        self.digit_0.x = 0
        self.append(self.digit_0)

        self.digit_1 = FlipDigit(
            self.static_spritesheet, self.static_spritesheet_palette,
            self.top_anim_spritesheet, self.top_anim_palette,
            self.bottom_anim_spritesheet, self.bottom_anim_palette,
            self.tile_width, self.tile_height, anim_delay=self.anim_delay,
            transparent_indexes=self.transparent_indexes,
            brighter_level=self.brighter_level, darker_level=self.darker_level, medium_level=self.medium_level
        )

        self.digit_1.x = self.tile_width
        self.append(self.digit_1)

        self.digit_2 = FlipDigit(
            self.static_spritesheet, self.static_spritesheet_palette,
            self.top_anim_spritesheet, self.top_anim_palette,
            self.bottom_anim_spritesheet, self.bottom_anim_palette,
            self.tile_width, self.tile_height, anim_delay=self.anim_delay,
            transparent_indexes=self.transparent_indexes,
            brighter_level=self.brighter_level, darker_level=self.darker_level, medium_level=self.medium_level
        )

        self.digit_2.x = (self.tile_width) * 2 + COLON_SPACE
        self.append(self.digit_2)

        self.digit_3 = FlipDigit(
            self.static_spritesheet, self.static_spritesheet_palette,
            self.top_anim_spritesheet, self.top_anim_palette,
            self.bottom_anim_spritesheet, self.bottom_anim_palette,
            self.tile_width, self.tile_height, anim_delay=self.anim_delay,
            transparent_indexes=self.transparent_indexes,
            brighter_level=self.brighter_level, darker_level=self.darker_level, medium_level=self.medium_level
        )

        self.digit_3.x = self.digit_2.x + self.tile_width
        self.append(self.digit_3)

        colon_palette = Palette(1)
        colon_palette[0] = 0xffffff
        colon_x = self.digit_1.x + self.tile_width + 6
        top_dot_y = self.tile_height * 2 // 3
        bottom_dot_y = (self.tile_height * 2 // 3) * 2

        top_circle = Circle(pixel_shader=colon_palette, radius=4, x=colon_x, y=top_dot_y)
        bottom_circle = Circle(pixel_shader=colon_palette, radius=4, x=colon_x, y=bottom_dot_y)
        self.append(top_circle)
        self.append(bottom_circle)

    def _validate_new_pair(self, new_pair):
        if not isinstance(new_pair, str) or not len(new_pair) in (1, 2):
            raise ValueError("Pair Value must be str with length 2")

        if len(new_pair) == 1:
            new_pair = f"0{new_pair}"

        return new_pair

    @property
    def first_pair(self):
        return f"{str(self.digit_0.value)}{str(self.digit_1.value)}"

    @first_pair.setter
    def first_pair(self, new_pair):
        new_pair = self._validate_new_pair(new_pair)
        if self.digit_0.value != int(new_pair[0]):
            self.digit_0.value = int(new_pair[0])
        if self.digit_1.value != int(new_pair[1]):
            self.digit_1.value = int(new_pair[1])

    @property
    def second_pair(self):
        return f"{str(self.digit_2.value)}{str(self.digit_3.value)}"

    @second_pair.setter
    def second_pair(self, new_pair):
        new_pair = self._validate_new_pair(new_pair)
        if self.digit_2.value != int(new_pair[0]):
            self.digit_2.value = int(new_pair[0])
        if self.digit_3.value != int(new_pair[1]):
            self.digit_3.value = int(new_pair[1])
