from files import EXT_CONST

class Menu:

    def __init__(self, button_titles, area_corners, max_rows=4, how_many_columns=1, space_between=10, parent_menu=None, force_button_resize=False):
        """
        ______________________________________________________________________

        button_titles: <list> --> [<str>, <str>, ... , <str>]

        area_corners: <tuple> --> (<int>, <int>, <int>, <int>)

        max_rows, space_between: <int>

        parent_menu: <Menu>

        force_button_resize = <bool>


        ---> None
        ______________________________________________________________________

        Initializes an instance of type 'Menu'.

        'button_titles' must be a non-empty tuple.

        'max_rows' cannot be an integer lower than 1.

        'area_corners' must be a tuple of exactly 4 integers as its values.
        """

        if button_titles == ():

            raise Exception("'button_titles' cannot be empty. Must be an iteration with names (strings) and must have a length of at least 1.")

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
    def sub_menu(cls, button_titles, corners, how_many_cols=1, space=10):
        """
        ______________________________________________________________________

        button_titles: <list> --> [<str>, <str>, ... , <str>]

        area_corners: <tuple> --> (<int>, <int>, <int>, <int>)

        how_many_columns: <int>


        ---> <Menu>
        ______________________________________________________________________

        It creates an instance of type 'Menu', but with the symbols for some buttons
        changed.
        """
        sub = cls(button_titles, corners, how_many_columns=how_many_cols, space_between=space)

        sub.pgup_button.msg = '^'
        sub.pgdn_button.msg = 'v'

        return sub

    def generate_buttons(self, titles_list, x_space, y_space, space_between=0):
        """
        ______________________________________________________________________

        titles_list: <list> -->  [<str>, <str>, ... , <str>]

        x_space, y_space, space_between: <int>


        ---> <list> --> [<Button>, <Button>, ... , <Button>]
        ______________________________________________________________________

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

    def update_buttons(self, page=1):
        """
        ______________________________________________________________________

        page: <int>


        ---> <list> --> [<Button>, <Button>, ... , <Button>]
        ______________________________________________________________________

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

    def change_page(self, to_next=True, forced=False):
        """
        ______________________________________________________________________

        to_next, forced: <bool>


        ---> None
        ______________________________________________________________________

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

class Timer:

    def __init__(self, init_time, message=''):
        """
        ______________________________________________________________________

        init_time: <int>

        message: <str>


        ---> None
        ______________________________________________________________________

        Initializes an instance of type 'Timer'.
        """
        self.initial_time = init_time
        self.current_time = init_time
        self.msg = message

    def __str__(self):
        """
        ______________________________________________________________________

        ---> <str>
        ______________________________________________________________________

        Returns a string with class information so it can be printed later.
        """
        return f"Initital Time: {self.initial_time} - Current Time: {self.current_time}{f'Message: {self.msg}' if self.msg != '' else ''}"

    def deduct(self, how_much):
        """
        ______________________________________________________________________

        how_much: <int>


        ---> None
        ______________________________________________________________________

        Descends the countdown subtracting 'how_much' time from 'self.current_time'.
        """
        self.current_time -= how_much

    def reset(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Resets the timer to its original value ('self.initial_value').
        """
        self.current_time = self.initial_time
        self.msg = ''

    def is_zero_or_less(self):
        """
        ______________________________________________________________________

        ---> <bool>
        ______________________________________________________________________

        Returns 'True' if the current time of the Timer reaches zero (0) or further, and 'False' otherwise.
        """
        return self.current_time <= 0

    def change_message(self, new_message):
        """
        ______________________________________________________________________

        new_message: <str>


        ---> None
        ______________________________________________________________________

        Changes the current message to a given new one.
        """
        self.msg = new_message

class SpringTimer:

    def __init__(self, floor, ceiling, where_to_start, is_it_adding=True):
        """
        ______________________________________________________________________

        floor, ceiling: <int>

        where_to_start, is_it_adding: <bool>


        ---> None
        ______________________________________________________________________

        Initializes an instance of type 'SpringTimer'.
        """
        
        if floor >= ceiling:

            raise Exception("'floor' parameter must NOT be greater or equal than 'ceiling'")

        if where_to_start < floor or where_to_start > ceiling:

            raise Exception(f"'where_to_start' parameter needs to be between {floor} and {ceiling} inclusive")

        self.floor = floor
        self.ceil = ceiling
        self.current = where_to_start
        self.adding = is_it_adding

    def __str__(self):
        """
        ______________________________________________________________________

        ---> <str>
        ______________________________________________________________________

        Returns a string with class information so it can be printed later.
        """
        return f"Current: {self.current} - Floor: {self.floor} - Ceiling: {self.ceil} - Is it adding: {self.adding}"

    def count(self, how_much=1):
        """
        ______________________________________________________________________

        how_much: <int>


        ---> None
        ______________________________________________________________________

        Advances the counting of the Timer, deducting if 'self.adding' is False, otherwise adding.
        """
        if self.adding:

            if self.current < self.ceil:

                self.current += how_much 
        else:

            if self.current > self.floor:

                self.current -= how_much

        if any((self.current <= self.floor, self.current >= self.ceil)):

            self.adding = not self.adding

class _Entity:

    def __init__(self, x1, y1, x2, y2):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Initializes an instance of type '_Entity'.

        This is a basic class that is not used by itself. It serves as superclass
        of many others.
        """
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def upper_left(self):
        """
        ______________________________________________________________________

        ---> <tuple> --> (<int>, <int>)
        ______________________________________________________________________

        Returns the UPPER LEFT coordinates of its hitbox.
        """
        return self.x1, self.y1

    def upper_right(self):
        """
        ______________________________________________________________________

        ---> <tuple> --> (<int>, <int>)
        ______________________________________________________________________

        Returns the UPPER RIGHT coordinates of its hitbox.
        """
        return self.x1, self.y1

    def bottom_left(self):
        """
        ______________________________________________________________________

        ---> <tuple> --> (<int>, <int>)
        ______________________________________________________________________

        Returns the BOTTOM LEFT coordinates of its hitbox.
        """
        return self.x1, self.y2

    def bottom_right(self):
        """
        ______________________________________________________________________

        ---> <tuple> --> (<int>, <int>)
        ______________________________________________________________________

        Returns the BOTTOM RIGHT coordinates of its hitbox.
        """
        return self.x2, self.y2

    def center(self):
        """
        ______________________________________________________________________

        ---> <tuple> --> (<int>, <int>)
        ______________________________________________________________________

        Return the CENTER coordinates of its hitbox.
        """
        return ((self.x2 + self.x1) // 2), ((self.y2 + self.y1) // 2)

class Button(_Entity):

    def __init__(self, x1, y1, x2, y2, message=''):
        """
        ______________________________________________________________________

        x1, y1, x2, y2: <int>

        message: <str>


        ---> None
        ______________________________________________________________________

        Initializes an instance of type 'Button'.
        """
        super().__init__(x1, y1, x2, y2)
        self.msg = message

    def __str__(self):
        """
        ______________________________________________________________________

        ---> <str>
        ______________________________________________________________________

        Returns a string with class information so it can be printed later.
        """
        return self.msg

class Ship(_Entity):

    def __init__(self, x1, y1, x2, y2, health=100, how_hard=0, speed=1, texture_path=None):
        """
        ______________________________________________________________________

        x1, y2, x2, y2, health, how_hard, speed: <int>

        texture_path: <str>


        ---> None
        ______________________________________________________________________

        Initializes an instance of type 'Ship'.
        """
        super().__init__(x1, y1, x2, y2)

        if self.is_out_bounds(x1, y1, x2, y2):

            raise Exception(f"Coordinates ({x1}, {y1}), ({x2}, {y2}) are not valid, as they are outside of the boundaries of the screen")

        self.max_hp = health
        self.hp = health
        self.hardness = how_hard
        self.speed = speed
        self.sprites = texture_path

    def __str__(self):
        """
        ______________________________________________________________________

        ---> <str>
        ______________________________________________________________________

        Returns a string with class information so it can be printed later.
        """
        return f"x1, y1, x2, y2: {self.x1}, {self.y1}, {self.x2}, {self.y2} - health: {self.hp} - hardness: {self.hardness} - speed: {self.speed} - sprites: {self.sprites}"

    def __repr__(self):
        """
        ______________________________________________________________________

        ---> <str>
        ______________________________________________________________________

        Returns a string with class information so it can be parsed 'as is' later.
        """
        return f"x1, y1, x2, y2: {self.x1}, {self.y1}, {self.x2}, {self.y2} - health: {self.hp} - hardness: {self.hardness} - speed: {self.speed} - sprites: {self.sprites}"

    def is_out_bounds(self, x1, y1, x2, y2):
        """
        ______________________________________________________________________

        x1, y1, x2, y2: <int>


        ---> <bool>
        ______________________________________________________________________

        Checks if an _Entity is out of the bounds of the screen.

        Return 'True' if so. Else returns 'False'.
        """
        width, height = EXT_CONST['WIDTH'] - EXT_CONST['GUI_SPACE'], EXT_CONST['HEIGHT']

        return any((x1 < 0, y1 < 0, x2 > width, y2 > height))

    def has_no_health(self):
        """
        ______________________________________________________________________

        ---> <bool>
        ______________________________________________________________________

        Returns 'True' if if the ship has 0 health points or less, and 'False' otherwise.
        """
        return self.hp <= 0

    def collides_with(self, other):
        """
        ______________________________________________________________________

        other: <Ship>


        ---> <bool>
        ______________________________________________________________________

        Tests if the hitbox of the ship is colliding with another given one. Returns a boolean.

        Although it is intended for other 'Ship' instances, it works with any subclass of '_Entity'.
        """
        # Test Upper Side
        if other.y1 < self.y1 < other.y2:

            # Test Upper-Left Corner
            if other.x1 < self.x1 < other.x2:

                return True
                
            # Test Upper-Right Corner
            if other.x1 < self.x2 < other.x2:

                return True

        # Test Bottom Side
        if other.y1 < self.y2 < other.y2:

            # Test Bottom-Left Corner
            if other.x1 < self.x1 < other.x2:

                return True

            # Test Bottom-Right Corner
            if other.x1 < self.x2 < other.x2:

                return True

        return False

    def transfer(self, dx, dy):
        """
        ______________________________________________________________________

        dx, dy: <int>


        ---> None
        ______________________________________________________________________

        Changes ship coordinates from '(x1, y1), (x2, y2)' to '(x1 + dx, y1 + dy), (x2 + dx, y2 + dy)'.
        """
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def move(self, dx, dy):
        """
        ______________________________________________________________________

        dx, dy: <int>


        ---> None
        ______________________________________________________________________

        Moves the player around inside the boundaries of the screen.
        """
        if not self.is_out_bounds(self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy):

            self.transfer(dx, dy)

class Enemy(Ship):

    def __init__(self, x1, y1, x2, y2, enemy_type):
        """
        ______________________________________________________________________

        x1, y1, x2, y2: <int>

        enemy_type: <str>


        ---> None
        ______________________________________________________________________

        Initializes an instance of type 'Enemy'.
        """
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.type = enemy_type if enemy_type in EXT_CONST["ENEMY_TYPES"] else EXT_CONST["ENEMY_TYPES"][0]

        self.generate_enemy()

    def generate_enemy(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Generates an enemy with predefined stats, based on which type it is.
        """
        if self.type in ("common1", "common2"):

            self.hp = 3
            self.hardness = 10
            self.speed = 3

            self.internal_timer = (SpringTimer(0, 30, 30) if self.type == "common2" else Timer(30))
            self.direction = 0 # 0 for "LEFT", 1 for "DOWN" and 2 for "RIGHT"

            self.sprites = None # for now

    def trajectory(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Defines the movement of an enemy base on its type.
        """
        if self.type == "common1":

            if self.internal_timer.is_zero_or_less():

                self.direction = (self.direction + 1) % 3
                self.internal_timer.reset()

            else:

                self.internal_timer.deduct(1)

            self.transfer((-self.speed if self.direction == 0 else (self.speed if self.direction == 2 else 0)),
                          ((self.speed // 2) if self.direction == 1 else 0))

        elif self.type == "common2":

            if self.internal_timer.current == self.internal_timer.floor:

                    self.direction += 1

            elif self.internal_timer.current == self.internal_timer.ceil:

                    self.direction -= 1

            elif self.internal_timer.current == self.internal_timer.ceil // 2:

                if self.internal_timer.adding:

                    self.direction = (self.direction + 1) % 3

                else:

                    self.direction = (self.direction + 2) % 3
            
            self.internal_timer.count()

            self.transfer((-self.speed if self.direction == 0 else (self.speed if self.direction == 2 else 0)),
                          ((self.speed // 2) if self.direction == 1 else 0))

class Bullet(Ship):

    def __init__(self, x1, y1, x2, y2, health=10, how_hard=0, speed=1, texture_path=None, acceleration=1, oscillation_time=30, bullet_type=EXT_CONST["BULLET_TYPES"][0], first_to_right=True):
        """
        ______________________________________________________________________

        x1, y1, x2, y2, health, how_hard, speed, acceleration, oscillation_time: <int>

        texture_path, bullet_type: <str>


        ---> None
        ______________________________________________________________________

        Initializes an instance of type 'Bullet'.
        """
        super().__init__(x1, y1, x2, y2, health, how_hard, speed, texture_path)
        self.accel = acceleration
        self.type = bullet_type if bullet_type in EXT_CONST["BULLET_TYPES"] else EXT_CONST["BULLET_TYPES"][0]

        if self.type == "normal_acc":

            self.accel_timer = Timer(oscillation_time)

        elif self.type == "sinusoidal_simple":

            self.oscillatation = SpringTimer(-oscillation_time, oscillation_time, (oscillation_time if first_to_right else -oscillation_time))

    def trajectory(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Defines the movement of the bullet based on its type.
        """
        if self.type == "normal_acc":

            if self.accel_timer.current_time > 0:
                self.accel_timer.deduct(1)
                self.accel += 0.3

            self.transfer(0, -self.speed * self.accel)

        elif self.type == "sinusoidal_simple":

            self.oscillatation.count()
            self.transfer((self.oscillatation.current * 0.1) * self.speed, -self.speed)