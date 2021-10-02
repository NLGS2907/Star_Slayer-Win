# STAR SLAYER

A project initially thought as a hobby for testing the single-file game library "Gamelib" (made by [Diego Essaya](https://github.com/dessaya)), which can be found [here.](https://github.com/dessaya/python-gamelib)

<hr style="height:30px"/>

* [ Proyect is currently **ON HIATUS** ]

<hr style="height:30px"/>

## Planned Features:


### Gameplay

As far as it was originally planned, *Star Slayer* is a "Shoot 'em all!" minigame in which you control a spaceship and destroy all enemies. Simple, right?

<img alt="gameplay_test" src="readme/gifs/test_gameplay.gif" height=600 width=550>
*(A mighty and playable gameplay may be far from enjoyable as of yet right now though)*
<br/>


### A ~_totally not boring_~ enjoyable menu!

Is very ~~_tasteless_~~ of minimalistic style, and you can interact with ease with its oversimplified options.

<img alt="menus_exaple" src="readme/gifs/menus.gif" height=600 width=550>

Brought to you by customizable classes made with amateur skills but somewhat manageable! Found on [objects.py](objects.py) file.

```Python
class Menu:
    """
    Class for defining a game menu.
    """

    def __init__(self, button_titles: StrList, area_corners: IntTuple, **kwargs: MenuDict) -> None:
        """
        Initializes an instance of type 'Menu'.

        The following kwargs are the only valid:

        'button_titles' must be a non-empty tuple.

        'max_rows' cannot be an integer lower than 1.

        'area_corners' must be a tuple of exactly 4 integers as its values.

        'parent_menu' is another instance of type 'Menu' that has this instance
        as its child.

        'force_button_resize' means if the menu must use all the space in the area
        it is specified, which can resize the buttons.
        """

        if button_titles == ():

            raise Exception("'button_titles' cannot be empty. Must be an iteration with names (strings) and must have a length of at least 1.")

        # Define default values
        max_rows = kwargs.get("max_rows", 4)
        how_many_columns = kwargs.get("how_many_columns", 1)
        space_between = kwargs.get("space_between", 10)
        parent_menu = kwargs.get("parent_menu", None)
        force_button_resize = kwargs.get("force_button_resize", False)

        if max_rows < 1:

            raise Exception("'max_rows' must be an integer of 1 or higher.")

        if not len(area_corners) == 4:

            raise Exception(f"area_corners has {len(area_corners)}. It must have exactly 4 integers as values.")

        button_titles = (button_titles.split("-=trash_value=-") if isinstance(button_titles, str) else list(button_titles))

        buttons_len = len(button_titles)

        how_many_rows = ((buttons_len // how_many_columns) if any((how_many_columns == 1, buttons_len % how_many_columns == 0)) else (buttons_len // how_many_columns) + 1)

        if force_button_resize and how_many_rows < max_rows:

            max_rows = how_many_rows

        # Measures
        self.area_x1, self.area_y1, self.area_x2, self.area_y2 = area_corners
        self.max_columns = how_many_columns
        self.max_rows = max_rows

        x_space = (self.area_x2 - self.area_x1) // self.max_columns
        y_space = (self.area_y2 - self.area_y1) // self.max_rows

        # Pages-related calculations
        self.max_pages = (((how_many_rows // self.max_rows) + 1) if all((not how_many_rows == self.max_rows, not how_many_rows % self.max_rows == 0)) else how_many_rows // self.max_rows)
        self.current_page = 1

        # Menu-related
        self.parent = parent_menu

        # Special Buttons
        self.pgup_button = Button((self.area_x2 + space_between), self.area_y1, self.area_x2 + (y_space // 2), (self.area_y1 + (y_space // 2)), "/\\")
        self.pgdn_button = Button((self.area_x2 + space_between), (self.area_y2 - (y_space // 2)), self.area_x2 + (y_space // 2), self.area_y2, "\/")
        self.return_button = Button(self.area_x1, self.area_y1 - (EXT_CONST["HEIGHT"] // 20), self.area_x1 + (EXT_CONST["WIDTH"] // 20), self.area_y1 - space_between, '<')

        # Button Lists
        self.buttons = self.generate_buttons(button_titles, x_space, y_space, space_between)
        self.buttons_on_screen = self.update_buttons()

        # Timers
        self.press_cooldown = Timer(20)

    @classmethod
    def sub_menu(cls, button_titles: StrList, corners: IntTuple, how_many_cols: int=1, space: int=10) -> "Menu":
        """
        It creates an instance of type 'Menu', but with the symbols for some buttons
        changed.
        """

        sub = cls(button_titles, corners, how_many_columns=how_many_cols, space_between=space)

        sub.pgup_button.msg = '^'
        sub.pgdn_button.msg = 'v'

        return sub

    def generate_buttons(self, titles_list: StrList, x_space: int, y_space: int, space_between: int=0) -> ButtonsList:
        """
        Generate buttons based on the effective area of the menu and the 'self.button_titles' list.
        'space_between' determines how much dead space there is between each button in said area.
        """

        buttons_list = list()
        cols_counter = 0
        rows_counter = 0

        for title in titles_list:

            cols_counter %= self.max_columns
            rows_counter %= self.max_rows

            x1 = (cols_counter * x_space) + self.area_x1 + (0 if cols_counter == 0 else space_between // 2)
            x2 = ((cols_counter + 1) * x_space) + self.area_x1 - (0 if cols_counter == (self.max_columns - 1) else space_between // 2)
            y1 = (rows_counter * y_space) + self.area_y1 + (0 if rows_counter == 0 else space_between // 2)
            y2 = ((rows_counter + 1) * y_space) + self.area_y1 - (0 if rows_counter == (self.max_rows - 1) else space_between // 2)

            buttons_list.append(Button(x1, y1, x2, y2, title))

            cols_counter += 1

            if cols_counter % self.max_columns == 0: # Go to next row only if the currnet column is filled first

                rows_counter += 1

        return buttons_list

    def update_buttons(self, page: int=1) -> ButtonsList:
        """
        Updates the buttons list if the menu changes pages.

        The page number must be between 1 and the max values for the pages.
        """

        if 1 > page or self.max_pages < page:

            raise Exception(f"Page number is {page}. It must be between 1 and {self.max_pages} inclusive.") 

        buttons_list = list()

        for i in range((page - 1) * self.max_columns * self.max_rows, page * self.max_columns * self.max_rows):

            if i < len(self.buttons):

                buttons_list.append(self.buttons[i])

        if self.current_page < self.max_pages:

            buttons_list.append(self.pgdn_button)
        
        if self.current_page > 1:

            buttons_list.append(self.pgup_button)

        if self.parent: # add return button only if it is the main menu or a sub menu

            buttons_list.append(self.return_button)

        return buttons_list

    def change_page(self, to_next: bool=True, forced: bool=False) -> None:
        """
        Changes the current page to the previous or next one, depending of the parameter 'to_next'.
        If the new page is outside of the number of pages, does nothing if 'forced' is False, otherwise it rotates between the pages.
        """
        if forced:

            new_page = (self.max_pages % self.current_page) + 1

        else:

            new_page = (self.current_page + 1 if to_next else self.current_page - 1)
        
        if 1 <= new_page <= self.max_pages:

            self.current_page = new_page
            self.buttons_on_screen = self.update_buttons(new_page)

```
<br/>

**Example call:**
```Python
main_menu = Menu(['Play', 'Options', 'About', 'Exit'],
                 (200,
                 EXT_CONST['HEIGHT'] // 2,
                 EXT_CONST['WIDTH'] - 200,
                 EXT_CONST['HEIGHT'] - 50))
```
<br/>

## Don't miss out!
<br/>

If you just happened to be as bored as I was to think of this, feel free to kill time contributing to the cause! Anyone can contribute, but it may
require a review from me or similar, as the rules protecting the main branch changes even so and then...
