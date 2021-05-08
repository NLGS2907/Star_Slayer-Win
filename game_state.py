import objects
from files import EXT_CONST, map_level, map_keys

class Game:

    def __init__(self, inital_power=1, cooldown_constant=30):
        width, height = EXT_CONST['WIDTH'], EXT_CONST['HEIGHT']

        self.self_level = 1
        self.level_dict = map_level(1)
        self.level_timer = objects.Timer(self.level_dict['total_time'])
        self.level_dict.pop('total_time')

        self.player = objects.Ship((width // 2) - 30, (height / 1.17) - 30, (width // 2) + 30, (height / 1.17) + 30, how_hard=1, speed=5, texture_path='sprites/player/star_player.gif')
        self.power_level = inital_power
        self.cool_cons = cooldown_constant
        self.invulnerability = objects.Timer(30 + (self.power_level * 5))
        self.shooting_cooldown = objects.Timer(self.cool_cons // self.power_level)
        self.enemies, self.bullets = list(), list()

        self.debug_cooldown = objects.Timer(20)
        self.show_debug_info = False

        self.menu_in_display = objects.main_menu
        self.is_in_game = False
        self.exit = False

    # ------------------------------
    # User Control Functions : BEGIN
    # ------------------------------

    def process_key(self, key):
        """
        Reads which keys were pressed
        """
        return map_keys().get(key)

    def process_action(self, action):
        """
        Receives an action and process it into its rightful instructions.
        """
        player = self.player

        if not self.is_in_game:

            if action == 'UNDO':
                if self.menu_in_display.parent:
                    self.menu_in_display = self.menu_in_display.parent

            elif action == 'EXIT':
                self.exit_self()

        else:
            if action == 'UP':
                player.move(0, -player.speed)

            elif action == 'DOWN':
                player.move(0, player.speed)

            elif action == 'LEFT':
                player.move(-player.speed, 0)

            elif action == 'RIGHT':
                player.move(player.speed, 0)

            elif action == 'SHOOT':
                if self.shooting_cooldown.is_zero_or_less():
                    self.shoot_bullets()
                    self.shooting_cooldown.reset()

            elif action == 'DEBUG':
                if self.debug_cooldown.is_zero_or_less():
                    self.show_debug_info = not self.show_debug_info
                    self.debug_cooldown.reset()

            elif action == 'UNDO':
                self.menu_in_display = objects.main_menu
                self.change_is_in_game()

    def process_click(self, x, y):
        """
        Receives the coordinates of a click and process it into its rightful instructions.
        """
        if not self.is_in_game:
            menu = self.menu_in_display
            for button in menu.buttons_on_screen:
                if button.x1 <= x <= button.x2 and button.y1 <= y <= button.y2:

                    if button.msg == 'Play':
                        self.change_is_in_game()

                    elif button.msg == 'Options':
                        self.menu_in_display = objects.options_menu

                    elif button.msg == 'About':
                        print(f"\n-=-=-=-=-=-=-=-=-=-=-\n\nStar Slayer (Pre-Alpha) - Franco 'NLGS' Lighterman\n-\nGamelib by Diego Essaya\n\n-=-=-=-=-=-=-=-=-=-=-\n")

                    elif button.msg == 'Exit':
                        self.exit_self()
                    
                    elif button.msg == '↑':
                        self.menu_in_display.change_page(False)

                    elif button.msg == '↓':
                        self.menu_in_display.change_page(True)

                    break

    # ------------------------------
    # User Control Functions : END
    # ------------------------------

    def level_up(self, how_much=1):
        """
        Increments by `how_much` the level of the self.
        """
        self.self_level += how_much
        self.level_dict = map_level(self.self_level)

    def power_up(self, how_much=1):
        """
        Increments by `how_much` the power of the player.
        """
        self.power_level += how_much
        self.shooting_cooldown.initial_time = self.cool_cons // self.power_level

    def shoot_bullets(self):
        """
        Shoots bullets from player.
        """
        player_center_x = self.player.center()[0]

        if self.power_level  == 1:
            self.bullets.append(objects.Bullet(player_center_x - 5, self.player.y1 + 30, player_center_x + 5, self.player.y1 + 20, how_hard=self.player.hardness, speed=2))

        elif self.power_level == 2:
            self.bullets.append(objects.Bullet(player_center_x - 5, self.player.y1 + 30, player_center_x + 5, self.player.y1 + 20, how_hard=self.player.hardness, speed=3, bullet_type='sinusoidal_simple', first_to_right=True))

    def exec_bul_trajectory(self):
        """
        Moves each bullet according to their trajectory.
        """
        for bullet in self.bullets:
            if self.player.collides_with(bullet):
                if bullet.hardness > self.player.hardness:
                    self.player.hp -= bullet.hardness
                    bullet.hp = 0
            for enem in self.enemies:
                if bullet.collides_with(enem):
                    enem.hp -= bullet.hardness
                    bullet.hp = 0
                    break

            if bullet.y2 < -50 or bullet.has_no_health():
                self.bullets.remove(bullet)

            bullet.trajectory()

    def exec_enem_trajectory(self):
        """
        Moves each enemy according to its defined behaviour.
        """
        for enem in self.enemies:
            if enem.has_no_health():
                self.enemies.remove(enem)

    def exec_lvl_script(self):
        """
        Reads the level dictionary timeline and executes the instructions detailed within.
        """
        for instant in self.level_dict:

            if int(instant) == self.level_timer.current_time:
                for action in self.level_dict[instant]:
                    self.enemies.append(objects.Ship(action['x1'], action['y1'], action['x2'], action['y2'], action['health'], action['hard'], action['speed'], action['texture']))
                
                self.level_dict.pop(instant)
                break

    def advance_game(self):
        """
        This function is that one of a wrapper, and advances the state of the self.
        """
        if self.is_in_game:
            self.menu_in_display = None
            self.exec_bul_trajectory()
            self.exec_enem_trajectory()
            self.exec_lvl_script()

            if not self.level_timer.is_zero_or_less():
                self.level_timer.deduct(1)

            if not self.shooting_cooldown.is_zero_or_less():
                self.shooting_cooldown.deduct(1)

            if not self.debug_cooldown.is_zero_or_less():
                self.debug_cooldown.deduct(1)

        else:
            self.show_debug_info = False


    def change_is_in_game(self):
        """
        Changes `self.is_in_game` to its opposite.
        """
        self.is_in_game = not self.is_in_game

    def exit_self(self):
        """
        Sets the control variable `self.exit` to `True` to exit the self.
        """
        self.exit = True