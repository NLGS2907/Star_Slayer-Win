from files import EXT_CONST

class Menu:

    def __init__(self, button_titles, area_corners, max_buttons=4, space_between=10, parent_menu=None):

        if button_titles == ():
            raise Exception("'button_titles' cannot be empty. Must be an iteration with names (strings) and must have a length of at least 1")

        if max_buttons < 1:
            raise Exception("'max_buttons' must be an integer of 1 or higher")

        buttons_len = len(button_titles)

        if buttons_len < max_buttons:
            max_buttons = buttons_len

        self.area_x1, self.area_y1, self.area_x2, self.area_y2 = area_corners

        self.max_buttons = max_buttons
        self.button_space = (self.area_y2 - self.area_y1) // self.max_buttons
        self.max_pages = (((buttons_len // self.max_buttons) + 1) if all((buttons_len != self.max_buttons, buttons_len % self.max_buttons != 0)) else buttons_len // self.max_buttons)
        self.current_page = 1
        self.parent = parent_menu

        self.pgup_button = Button((self.area_x2 + space_between), self.area_y1, self.area_x2 + (self.button_space // 2), (self.area_y1 + (self.button_space // 2)), '↑')
        self.pgdn_button = Button((self.area_x2 + space_between), (self.area_y2 - (self.button_space // 2)), self.area_x2 + (self.button_space // 2), self.area_y2, '↓')

        self.buttons = self.generate_buttons(button_titles, space_between)
        self.buttons_on_screen = self.update_buttons()

    def generate_buttons(self, titles_list, space_between=0):
        """
        Generate buttons based on the effective area of the menu and the `self.button_titles` list.
        `space_between` determines how much dead space there is between each button in said area.
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
        Updates the buttons list if the menu changes pages.
        """
        buttons_list = list()

        for i in range((page - 1) * self.max_buttons, page * self.max_buttons):
            if i < len(self.buttons):
                buttons_list.append(self.buttons[i])

        if self.current_page < self.max_pages:
            buttons_list.append(self.pgdn_button)
        
        if self.current_page > 1:
            buttons_list.append(self.pgup_button)

        return buttons_list

    def change_page(self, to_next=True, forced=False):
        """
        Changes the current page to the previous or next one, depending of the parameter `to_next`.
        If the new page is outside of the number of pages, does nothing if `forced` is False, otherwise it rotates between the pages.
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
        self.initial_time = init_time
        self.current_time = init_time
        self.msg = message

    def __str__(self):

        return f"Initital Time: {self.initial_time} - Current Time: {self.current_time}{f'Message: {self.msg}' if self.msg != '' else ''}"

    def deduct(self, how_much):
        """
        Descends the countdown subtracting `how_much` time from `self.current_time`.
        """
        self.current_time -= how_much

    def reset(self):
        """
        Resets the timer to its original value (`self.initial_value`).
        """
        self.current_time = self.initial_time
        self.msg = ''

    def is_zero_or_less(self):
        """
        Returns `True` if the current time of the Timer reaches zero (0) or further, and `False` otherwise.
        """
        return self.current_time <= 0

    def change_message(self, new_message):
        """
        Changes the current message to a given new one.
        """
        self.msg = new_message

class SpringTimer:

    def __init__(self, floor, ceiling, where_to_start, is_it_adding=True):
        
        if floor >= ceiling:
            raise Exception("'floor' parameter must NOT be greater or equal than 'ceiling'")

        if where_to_start < floor or where_to_start > ceiling:
            raise Exception(f"'where_to_start' parameter needs to be between {floor} and {ceiling} inclusive")

        self.floor = floor
        self.ceil = ceiling
        self.current = where_to_start
        self.adding = is_it_adding

    def __str__(self):
        
        return f"Current: {self.current} - Floor: {self.floor} - Ceiling: {self.ceil} - Is it adding: {self.adding}"

    def count(self, how_much=1):
        """
        Advances the counting of the Timer, deducting if `self.adding` is False, otherwise adding.
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
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def upper_left(self):
        """
        Returns the UPPER LEFT coordinates of its hitbox.
        """
        return self.x1, self.y1

    def upper_right(self):
        """
        Returns the UPPER RIGHT coordinates of its hitbox.
        """
        return self.x1, self.y1

    def bottom_left(self):
        """
        Returns the BOTTOM LEFT coordinates of its hitbox.
        """
        return self.x1, self.y2

    def bottom_right(self):
        """
        Returns the BOTTOM RIGHT coordinates of its hitbox.
        """
        return self.x2, self.y2

    def center(self):
        """
        Return the CENTER coordinates of its hitbox.
        """
        return ((self.x2 + self.x1) // 2), ((self.y2 + self.y1) // 2)

class Button(_Entity):

    def __init__(self, x1, y1, x2, y2, message=''):

        super().__init__(x1, y1, x2, y2)
        self.msg = message

class Ship(_Entity):

    def __init__(self, x1, y1, x2, y2, health=500, how_hard=0, speed=1, texture_path=None):

        super().__init__(x1, y1, x2, y2)

        if self.is_out_bounds(x1, y1, x2, y2):
            raise Exception(f"Coordinates ({x1}, {y1}), ({x2}, {y2}) are not valid, as they are outside of the boundaries of the screen")

        self.hp = health
        self.hardness = how_hard
        self.speed = speed
        self.sprites = texture_path

    def __str__(self):

        return f"x1, y1, x2, y2: {self.x1}, {self.y1}, {self.x2}, {self.y2} - health: {self.hp} - hardness: {self.hardness} - speed: {self.speed} - sprites: {self.sprites}"

    def __repr__(self):

        return f"x1, y1, x2, y2: {self.x1}, {self.y1}, {self.x2}, {self.y2} - health: {self.hp} - hardness: {self.hardness} - speed: {self.speed} - sprites: {self.sprites}"

    def is_out_bounds(self, x1, y1, x2, y2):
        """
        Checks if an _Entity is out of the bounds of the screen.
        """
        width, height = EXT_CONST['WIDTH'] - EXT_CONST['GUI_SPACE'], EXT_CONST['HEIGHT']

        return any((x1 < 0, y1 < 0, x2 > width, y2 > height))

    def has_no_health(self):
        """
        Returns `True` if if the ship has 0 health points or less, and `False` otherwise.
        """
        return self.hp <= 0

    def collides_with(self, other):
        """
        Tests if the hitbox of the ship is colliding with another given one. Returns a boolean.
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
        Changes ship coordinates from `(x1, y1), (x2, y2)` to `(x1 + dx, y1 + dy), (x2 + dx, y2 + dy)`.
        """
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def move(self, dx, dy):
        """
        Moves the player around inside the bounds of the screen.
        """
        if not self.is_out_bounds(self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy):
            self.transfer(dx, dy)

class Bullet(Ship):

    def __init__(self, x1, y1, x2, y2, health=10, how_hard=0, speed=1, texture_path=None, acceleration=1, oscillation_time=30, bullet_type='normal_acc', first_to_right=True):

        super().__init__(x1, y1, x2, y2, health, how_hard, speed, texture_path)
        self.accel = acceleration
        self.type = bullet_type if bullet_type in ('normal_acc', 'sinusoidal_simple') else 'normal_acc'

        if self.type == 'normal_acc':
            self.accel_timer = Timer(oscillation_time)

        if self.type == 'sinusoidal_simple':
            self.oscillatation = SpringTimer(-oscillation_time, oscillation_time, (oscillation_time if first_to_right else -oscillation_time))

    def trajectory(self):
        """
        Defines he movement of the bullet based on its type.
        """
        if self.type == 'normal_acc':
            if self.accel_timer.current_time > 0:
                self.accel_timer.deduct(1)
                self.accel += 0.3
            self.transfer(0, -self.speed * self.accel)

        elif self.type == 'sinusoidal_simple':
            self.oscillatation.count()
            self.transfer((self.oscillatation.current * 0.1) * self.speed, -self.speed)

main_menu = Menu(('Play', 'Options', 'About', 'Exit'), (200, EXT_CONST['HEIGHT'] // 2, EXT_CONST['WIDTH'] - 200, EXT_CONST['HEIGHT'] - 50))
options_menu = Menu(('Option_01', 'Option_02', 'Option_03', 'Option_04', 'Option_05', 'Option_06', 'Option_07', 'Option_08', 'Option_09', 'Option_10', 'Option_11', 'Option_12'), (200, EXT_CONST['HEIGHT'] // 2, EXT_CONST['WIDTH'] - 200, EXT_CONST['HEIGHT'] - 50), max_buttons=3, parent_menu=main_menu)