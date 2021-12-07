"""
Selector Module. This stores a color selector
that helps the user in picking a color.
"""

from typing import Optional
from colorsys import hsv_to_rgb

from .utils import IntTuple

CoordsTuple = Optional[tuple[int, int]]
ColorsDict = dict[CoordsTuple, str]
RGBTuple = tuple[int, int, int]


class ColorSelector():
    """
    Class for a Color Picker.
    """

    def __init__(self,
                 *,
                 area: IntTuple,
                 palette_area: Optional[IntTuple]=None,
                 cols: int=10,
                 rows: int=7) -> None:
        """
        Creates an instace of 'ColorSelector'.
        """

        self._validate_area(area)        

        if not palette_area:

            palette_area = area

        else:

            self._validate_area(palette_area)

        self._validate_areas_boundaries(area, palette_area)

        self.x1, self.y1, self.x2, self.y2 = area
        self.p_x1, self.p_y1, self.p_x2, self.p_y2 = palette_area

        self.rows: int = rows
        self.cols: int = cols

        # HSV Attributes
        self.hue: float = 0
        self.hue_bar: list[str] = self.generate_hue_bar()

        self.color_palette: ColorsDict= self.generate_colors()

        self.selection: CoordsTuple = None


    @property
    def area(self) -> IntTuple:
        """
        Returns the coordinates of the selector area.
        """

        return (self.x1, self.y1, self.x2, self.y2)


    @property
    def palette_area(self) -> IntTuple:
        """
        Returns the coordinates of the palette area.
        """

        return (self.p_x1, self.p_y1, self.p_x2, self.p_y2)


    def _validate_16_bit(self, number: int) -> None:
        """
        The number must be an integer between 0 and 255.

        It raises 'ValueError' if that is the case.
        """

        if any((number < 0, 255 < number)):

            raise ValueError(f"Decimal Number '{number}' is not a number between 0 and 255.")


    def _validate_area(self, area: IntTuple) -> None:
        """
        An area must be a tuple of exactly 4 (four) integers.

        This raises 'ValueError' if that is not the case.
        """

        if not len(area) == 4:

            raise ValueError(f"area has {len(area)} values. It must be 4 integers or floats.")


    def _validate_areas_boundaries(self, larger_area: IntTuple, smaller_area: IntTuple) -> bool:
        """
        The smaller area must always be inside the boundaries of the larger one.

        This function returns 'True' if that is the case, otherwise returns 'False'.
        """

        ...


    def dec_to_hex(self, red: int, green: int, blue: int) -> str:
        """
        Converts the format '(rr, gg, bb)' to a string of type
        '#rrggbb'.
        """

        return f"#{red:02x}{green:02x}{blue:02x}"


    def hex_to_dec(self, hex: str) -> RGBTuple:
        """
        Converts the format '#rrggbb' to a string of type
        '(rr, gg, bb)'.
        """

        if not len(hex) == 7:

            raise ValueError(f"hex number '{hex}' is invalid (it has not a length of 7).")


        dec = list()

        for i in range(0, 6, 2):

            hex_number = hex[1:][i:i + 2]
            dec.append(int(hex_number, 16))

        for dec_number in dec:

            self._validate_16_bit(dec_number)    

        return tuple(dec_number)


    def dec_float_to_int(self, rgb_floats: tuple[float, float, float]) -> RGBTuple:
        """
        Converts a tuple of RGB values in float form to its integer variant.
        """

        return tuple(int(color * 255) for color in rgb_floats)


    def generate_colors(self, rows: int=0, cols: int=0) -> ColorsDict:
        """
        Creates the color palette.
        """

        if not rows:

            rows = self.rows

        if not cols:

            cols = self.cols

        s_augment = 1.0 / cols
        v_augment = 1.0 / rows

        colors = dict()

        for row in range(rows):

            value = 1.0 - (v_augment * row) # We want black to be on bottom

            for col in range(cols):

                saturation = (s_augment * col)
                red, green, blue = self.dec_float_to_int(hsv_to_rgb(self.hue, saturation, value))

                colors[(col, row)] = self.dec_to_hex(red, green, blue)

        return colors


    def generate_hue_bar(self, size=100) -> list[str]:
        """
        Generates a bar with a lot of possible hue values.
        """

        bar = list()
        hue = 0.0

        for _ in range(size):

            red, green, blue = self.dec_float_to_int(hsv_to_rgb(hue, 1.0, 1.0))
            color = self.dec_to_hex(red, green, blue)

            bar.append(color)
            hue += (1.0 / size)

        return bar
