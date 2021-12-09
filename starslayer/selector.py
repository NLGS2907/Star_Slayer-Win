"""
Selector Module. This stores a color selector
that helps the user in picking a color.
"""

from typing import Callable, Optional
from colorsys import hsv_to_rgb

from starslayer.files import StrDict

from .gamelib import input, say
from .utils import ButtonsList, IntTuple, Button
from .consts import HEIGHT, WIDTH

CoordsTuple = tuple[int, int]
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
                 rows: int=7,
                 hue_bar_size: int=100) -> None:
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
        self._hue_index: int = 0
        self.generate_hue_bar(hue_bar_size)

        self.generate_colors()

        self.selection: CoordsTuple = ((self.cols - 1), 0)
        self.generate_buttons()

        # Control Booleans
        self.is_transparent = False
        self.next: bool = False
        self.exit: bool = False


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


    @property
    def augment_x(self) -> float:
        """
        Returns the augment of the X axis.
        """

        return (self.p_x2 - self.p_x1) / self.cols


    @property
    def augment_y(self) -> float:
        """
        Returns the augment of the Y axis.
        """

        return  (self.p_y2 - self.p_y1) / self.rows


    @property
    def hue_index(self) -> int:

        return self._hue_index

    @hue_index.setter
    def hue_index(self, new_index: int) -> None:

        self._hue_index = new_index
        self.generate_colors()


    @property
    def hue_bar_area(self) -> IntTuple:
        """
        Returns the corners of the hue bar area.
        """

        aux_x = (WIDTH // 150)
        aux_y = (HEIGHT // 140)

        return (self.p_x1 + (2 * aux_x),
                self.p_y2 + (3 * aux_y),
                self.p_x2 - (2 * aux_x),
                self.p_y2 + (7 * aux_y))

    @property
    def inv_color_area(self) -> IntTuple:
        """
        Returns the corners of the area of a button
        made to select no color.
        """

        aux_x = (WIDTH // 150)
        aux_y = (HEIGHT // 140)

        return (self.x1 + (25 * aux_x),
                self.y2 - (11 * aux_y),
                self.x1 + (34 * aux_x),
                self.y2 - (2 * aux_y))


    @property
    def hue_augment(self) -> None:
        """
        Returns the augment of the hue bar.
        """

        x1, _, x2, _ = self.hue_bar_area

        return (x2 - x1) / len(self.hue_bar)


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

        x1, y1, x2, y2 = larger_area
        p_x1, p_y1, p_x2, p_y2 = smaller_area

        if any((p_x1 < x1,
                p_y1 < y1,
                x2 < p_x2,
                y2 < p_y2)):

            raise ValueError(f"Smaller area '{smaller_area}' is not inside the boundaries of the greater area '{larger_area}'.")


    def _validate_hex(self, hex: str) -> bool:
        """
        Returns 'True' if hex if a string of the pattern
        '#rrggbb'.

        Otherwise, returns 'False'.
        """

        if not len(hex) == 7 or not hex.startswith('#'):
            return False

        for i in hex[1:]:

            if i not in "0123456789abcdefABCDEF":

                return False

        return True


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

        if not self._validate_hex(hex):

            raise ValueError(f"hex number '{hex}' is invalid.")

        dec = []

        for i in range(0, 6, 2):

            hex_number = hex[1:][i:i + 2]
            dec.append(int(hex_number, 16))

        for dec_number in dec:

            self._validate_16_bit(dec_number)    

        return tuple(dec)


    def dec_float_to_int(self, rgb_floats: tuple[float, float, float]) -> RGBTuple:
        """
        Converts a tuple of RGB values in float form to its integer variant.
        """

        return tuple(int(color * 255) for color in rgb_floats)


    def generate_colors(self, rows: int=0, cols: int=0) -> None:
        """
        Creates the color palette.
        """

        if not rows:

            rows = self.rows

        if not cols:

            cols = self.cols

        s_augment = 1.0 / cols
        v_augment = 1.0 / rows

        colors: ColorsDict = {}

        for row in range(rows):

            value = 1.0 - (v_augment * row) # We want black to be on bottom

            for col in range(cols):

                hue, _ = self.hue_bar[self.hue_index]
                saturation = (s_augment * col)

                red, green, blue = self.dec_float_to_int(hsv_to_rgb(hue, saturation, value))

                colors[(col, row)] = self.dec_to_hex(red, green, blue)

        setattr(self, "color_palette", colors)


    def get_selected_color(self) -> str:
        """
        Returns a string of type '#rrggbb' which
        is the color selected.
        """

        return ('' if self.is_transparent else self.color_palette[self.selection])


    def generate_hue_bar(self, size) -> None:
        """
        Generates a bar with a lot of possible hue values.
        """

        bar: list[str] = []
        hue = 0.0

        for _ in range(size):

            red, green, blue = self.dec_float_to_int(hsv_to_rgb(hue, 1.0, 1.0))
            color = self.dec_to_hex(red, green, blue)

            bar.append((hue, color))
            hue += (1.0 / size)

        setattr(self, "hue_bar", bar)


    def generate_buttons(self) -> None:
        """
        Creates the buttons, the function assigned to them,
        and adds everything to dictionaries that contain them.
        """

        buttons: ButtonsList = []
        actions: dict[str, Callable] = {}

        aux = (WIDTH / 75)
        upper = self.y2 - (HEIGHT * 0.078571)
        bottom = self.y2 - (HEIGHT / 70)

        apply_button = Button(self.x2 - (22 * aux), upper, self.x2 - (12 * aux), bottom, "Apply")
        buttons.append(apply_button)

        # -------------------------------------------------- #
        def apply_color(profile: StrDict, attribute: str) -> None:
            """
            Applies the selected color.
            """

            profile[attribute] = self.get_selected_color()
            self.exit_selector()

        actions[apply_button.msg] = apply_color
        # -------------------------------------------------- #

        cancel_button = Button(self.x2 - (11 * aux), upper, self.x2 - aux, bottom, "Cancel")
        buttons.append(cancel_button)

        # -------------------------------------------------- #
        def cancel_selection(profile: StrDict, attribute: str) -> None:
            """
            Cancel the selection and exit the prompt.
            """

            self.exit_selector()

        actions[cancel_button.msg] = cancel_selection
        # -------------------------------------------------- #

        input_button = Button(self.x1 + aux, upper, self.x1 + (11* aux), bottom, "Input")
        buttons.append(input_button)

        # -------------------------------------------------- #
        def input_color(profile: StrDict, attribute: str) -> None:
            """
            Prompts the user for a box where they input a custom color in the Pattern
            '#rrggbb' or 'rrggbb'.
            """

            selected_color = input("Please enter a color in hexadecimal format (#rrggbb)")
            hex = None

            if not selected_color:

                return

            if self._validate_hex(selected_color):

                hex = selected_color

            elif self._validate_hex(f"#{selected_color}"):

                hex = f"#{selected_color}"

            if hex:

                profile[attribute] = hex
                self.exit_selector()

            else:

                say(f"'{selected_color}' is an invalid HEX color")

        actions[input_button.msg] = input_color
        # -------------------------------------------------- #

        setattr(self, "buttons", buttons)
        setattr(self, "actions", actions)


    def clicked_inside_area(self, x: int, y: int, area: IntTuple) -> bool:
        """
        Returns 'True' if the click coordinates are inside
        the corners of a given area.

        Otherwise, returns 'False'.
        """

        x1, y1, x2, y2 = area

        return all((x1 <= x,
                    y1 <= y,
                    x <= x2,
                    y <= y2))


    def search_matrix_indexes(self, px_x: int, px_y: int) -> CoordsTuple:
        """
        Given a click coordinates in pixels, it searches through
        the color table and returns the corresponding indexes.
        """

        x = (px_x - self.p_x1) / self.augment_x
        y = (px_y - self.p_y1) / self.augment_y

        return int(x), int(y)


    def search_hue_index(self, px_x: int) -> int:
        """
        Searches through the hue bar, and returns the index that
        corresponds to the click coordinates.
        """

        hue_x1, _, _, _ = self.hue_bar_area

        return int((px_x - hue_x1) / self.hue_augment)


    def click(self, x: int, y: int, profile: StrDict, attribute: str) -> None:
        """
        Processes the click and executes the logic of a
        button, were the coordinates (x, y) inside of
        its boundaries.
        """

        if self.clicked_inside_area(x, y, self.palette_area):

            self.is_transparent = False
            i, j = self.search_matrix_indexes(x, y)
            self.selection = (i, j)

            self.next_iteration()
            return

        if self.clicked_inside_area(x, y, self.hue_bar_area):

            self.is_transparent = False
            self.hue_index = self.search_hue_index(x)

            self.next_iteration()
            return

        if self.clicked_inside_area(x, y, self.inv_color_area):

            self.is_transparent = True

            self.next_iteration()
            return

        for button in self.buttons:

            if button.is_inside(x, y):

                func = self.actions.get(button.msg, None)
                if func: func(profile, attribute)


    def reset(self) -> None:
        """
        Resets the hue and the selection to their
        default values.
        """

        self.is_transparent = False
        self.selection = ((self.cols - 1), 0)
        self.hue_index = 0


    def next_iteration(self) -> None:
        """
        Exits the selector, but reopens it to
        refresh it.
        """

        self.next = True

    def exit_selector(self) -> None:
        """
        Prepares the selector to exit the prompt.
        """

        self.reset()
        self.exit = True
