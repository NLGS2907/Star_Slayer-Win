from files import EXT_CONST

class Menu:

    def __init__(self, button_titles, area_corners, max_buttons=4, space_between=10, parent_menu=None, force_button_resize=False, is_sub=False):
        """
        ______________________________________________________________________

        button_titles: <list> --> [<str>, <str>, ... , <str>]

        area_corners: <tuple> --> (<int>, <int>, <int>, <int>)

        max_buttons, space_between: <int>

        parent_menu: <Menu>

        force_button_resize, is_sub = <bool>


        ---> None
        ______________________________________________________________________

        Initializes an instance of type 'Menu'.

        'button_titles' must be a non-empty tuple.

        'max_buttons' cannot be an integer lower than 1.

        'area_corners' must be a tuple of exactly 4 integers as its values.
        """

        if button_titles == ():

            raise Exception("'button_titles' cannot be empty. Must be an iteration with names (strings) and must have a length of at least 1")

        if max_buttons < 1:

            raise Exception("'max_buttons' must be an integer of 1 or higher")

        if not len(area_corners) == 4:

            raise Exception(f"'area_corners has {len(area_corners)}. It must have exactly 4 integers as values'")

        button_titles = (button_titles.split("-=trash_value=-") if isinstance(button_titles, str) else list(button_titles))

        buttons_len = len(button_titles)

        if force_button_resize and buttons_len < max_buttons:

            max_buttons = buttons_len

        self.area_x1, self.area_y1, self.area_x2, self.area_y2 = area_corners

        self.max_buttons = max_buttons
        self.button_space = (self.area_y2 - self.area_y1) // self.max_buttons
        self.max_pages = (((buttons_len // self.max_buttons) + 1) if all((buttons_len != self.max_buttons, buttons_len % self.max_buttons != 0)) else buttons_len // self.max_buttons)
        self.current_page = 1
        self.parent = parent_menu

        self.pgup_button = Button((self.area_x2 + space_between), self.area_y1, self.area_x2 + (self.button_space // 2), (self.area_y1 + (self.button_space // 2)), ('🠕' if is_sub else '↑'))
        self.pgdn_button = Button((self.area_x2 + space_between), (self.area_y2 - (self.button_space // 2)), self.area_x2 + (self.button_space // 2), self.area_y2, ('🠗' if is_sub else '↓'))
        self.return_button = Button(self.area_x1, self.area_y1 - (EXT_CONST["HEIGHT"] // 20), self.area_x1 + (EXT_CONST["WIDTH"] // 20), self.area_y1 - space_between, '←')

        self.buttons = self.generate_buttons(button_titles, space_between)
        self.buttons_on_screen = self.update_buttons()

        self.press_cooldown = Timer(20)

    def generate_buttons(self, titles_list, space_between=0):
        """
        ______________________________________________________________________

        titles_list: <list> -->  [<str>, <str>, ... , <str>]

        space_between: <int>


        ---> <list> --> [<Button>, <Button>, ... , <Button>]
        ______________________________________________________________________

        Generate buttons based on the effective area of the menu and the 'self.button_titles' list.
        'space_between' determines how much dead space there is between each button in said area.
        """
        buttons_list = list()
        counter = 0

        for title in titles_list:

            counter %= self.max_buttons
            x1, x2 = self.area_x1, self.area_x2
            y1 = (counter * self.button_space) + self.area_y1 + (0 if counter == 0 else space_between // 2)
            y2 = ((counter + 1) * self.button_space) + self.area_y1 - (0 if counter == (self.max_buttons - 1) else space_between // 2)

            buttons_list.append(Button(x1, y1, x2, y2, title))

            counter += 1

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

        for i in range((page - 1) * self.max_buttons, page * self.max_buttons):

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

    def __init__(self, x1, y1, x2, y2, health=500, how_hard=0, speed=1, texture_path=None):
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
        if self.type == "common":

            self.hp = 3
            self.hardness = 10
            self.speed = 3

            self.internal_timer = Timer(30)
            self.direction = 0 # 0 for "LEFT", 1 for "DOWN" and 2 for "RIGHT"

            self.sprites = None # for now

    def trajectory(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Defines the movement of an enemy base on its type.
        """
        if self.type == "common":

            if self.internal_timer.is_zero_or_less():

                self.direction = (self.direction + 1) % 3
                self.internal_timer.reset()

            else:

                self.internal_timer.deduct(1)

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