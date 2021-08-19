import gamelib, objects, files

class Game:

    def __init__(self, inital_power=1, cooldown_constant=30):
        """
        ______________________________________________________________________

        initial_power, cooldown_constant: <int>


        ---> None
        ______________________________________________________________________

        Initalizes the 'Game' class.
        """

        width, height = files.EXT_CONST["WIDTH"], files.EXT_CONST["HEIGHT"]

        self.main_menu = objects.Menu(["Play", "Options", "About", "Exit"],
                         (200, height // 2, width - 200, height - 50))

        self.options_menu = objects.Menu(["Configure Controls", "Change Color Profile (WIP)"],
                                    (200, height // 2, width - 200, height - 50), max_buttons=4, parent_menu=self.main_menu)

        self.controls_menu = objects.Menu(files.list_actions(),
                                    (10, (height // 5), (width // 4) - 10, height - 10), max_buttons=8, parent_menu=self.options_menu)

        self.game_level = 1
        self.level_dict = files.map_level(1)
        self.level_timer = objects.Timer(self.level_dict["total_time"])
        self.level_dict.pop("total_time")

        self.player = objects.Ship((width // 2) - 30, int(height / 1.17) - 30, (width // 2) + 30, int(height / 1.17) + 30, how_hard=1, speed=5, texture_path=('sprites/player/star_player.gif','sprites/player/star_player_damaged.gif'))
        self.power_level = inital_power
        self.cool_cons = cooldown_constant
        self.invulnerability = objects.Timer(50 + (self.power_level * 5))
        self.shooting_cooldown = objects.Timer(self.cool_cons // self.power_level)
        self.enemies, self.bullets = list(), list()

        self.debug_cooldown = objects.Timer(20)
        self.show_debug_info = False

        self.menu_in_display = self.main_menu
        self.action_to_show = files.list_actions()[0]
        self.sub_menu = self.refresh_sub_menu()

        self.is_in_game = False
        self.show_about = False
        self.exit = False

    # ------------------------------ #
    # User Control Functions : BEGIN #
    # ------------------------------ #

    def process_key(self, key):
        """
        ______________________________________________________________________

        key: <str>


        ---> <str>
        ______________________________________________________________________
        
        Reads which key was released, and returns its corresponding action.
        """
        return files.map_keys().get(key)

    def process_action(self, action):
        """
        ______________________________________________________________________

        action: <str>


        ---> None
        ______________________________________________________________________

        Receives an action and process it into its rightful instructions.
        """
        player = self.player

        if not self.is_in_game:

            if action == "RETURN":

                if self.show_about:

                    self.show_about = False

                elif self.menu_in_display.parent and self.menu_in_display.press_cooldown.is_zero_or_less():

                    self.menu_in_display.press_cooldown.reset() # First we reset the current menu
                    self.menu_in_display = self.menu_in_display.parent
                    self.menu_in_display.press_cooldown.reset() # Then the parent

            elif action == "EXIT":

                self.exit_game()

        else:

            if action == "UP":

                player.move(0, -player.speed)

            elif action == "DOWN":

                player.move(0, player.speed)

            elif action == "LEFT":

                player.move(-player.speed, 0)

            elif action == "RIGHT":

                player.move(player.speed, 0)

            elif action == "SHOOT":

                if self.shooting_cooldown.is_zero_or_less():

                    self.shoot_bullets()
                    self.shooting_cooldown.reset()

            elif action == "DEBUG":

                if self.debug_cooldown.is_zero_or_less():

                    self.show_debug_info = not self.show_debug_info
                    self.debug_cooldown.reset()

            elif action == "RETURN":

                if self.show_about:

                    self.show_about = False
                
                else:

                    self.menu_in_display = self.main_menu
                    self.change_is_in_game()
                    self.clear_assets()

    def process_click(self, x, y):
        """
        ______________________________________________________________________

        x, y: <int>


        ---> None
        ______________________________________________________________________

        Receives the coordinates of a click and process it into its rightful instructions.
        """
        if all((not self.is_in_game, not self.show_about)):

            menu = self.menu_in_display

            for button in (menu.buttons_on_screen + self.sub_menu.buttons_on_screen):

                if button.x1 <= x <= button.x2 and button.y1 <= y <= button.y2:

                    if all((self.menu_in_display == self.controls_menu, button.msg in files.list_actions(), not self.action_to_show == button.msg)):

                        self.action_to_show = button.msg
                        self.sub_menu = self.refresh_sub_menu()

                    else:

                        if button.msg == "Play":

                            self.change_is_in_game()

                        elif button.msg == "Options":

                            self.menu_in_display = self.options_menu

                        elif button.msg == "About":

                            self.show_about = True

                        elif button.msg == "Exit":

                            self.exit_game()

                        elif button.msg == '←':

                            self.process_action("RETURN")
                        
                        elif button.msg == '↑':

                            self.menu_in_display.change_page(False)

                        elif button.msg == '↓':

                            self.menu_in_display.change_page(True)

                        elif button.msg == '🠕':

                            self.sub_menu.change_page(False)

                        elif button.msg == '🠗':

                            self.sub_menu.change_page(True)

                        elif button.msg == "Configure Controls":

                            self.menu_in_display = self.controls_menu

                        elif button.msg in (f"Change {key}" for key in files.map_keys().keys()):
                            
                            print(f"'Change Key' was pressed!")
                            pass

                        elif button.msg == "Add Key":

                            new_dict, success = self.add_key(self.action_to_show)

                            if success:

                                files.print_keys(new_dict)
                                self.sub_menu = self.refresh_sub_menu()

                    break

    def add_key(self, action):
        """
        ______________________________________________________________________

        action: <str>


        ---> <tuple> --> (<dict>, <bool>)
        ______________________________________________________________________

        If valid, adds a key to a designed action.
        Return the dictionary of the keys, plus 'True' if the function
        succeeded, else 'False' if something happened.
        """
        event = gamelib.wait(gamelib.EventType.KeyRelease)

        keys_dict = files.map_keys()

        if event.key in keys_dict:

            return keys_dict, False

        keys_dict[event.key] = action

        return keys_dict, True

    # ------------------------------ #
    # User Control Functions : END   #
    # ------------------------------ #

    def refresh_sub_menu(self, x1=(files.EXT_CONST["WIDTH"] // 4) + 30,
                               y1=(files.EXT_CONST["HEIGHT"] // 2),
                               x2=(files.EXT_CONST["WIDTH"] * (5 / 8)),
                               y2=(files.EXT_CONST["HEIGHT"] - 10)):
        """
        ______________________________________________________________________

        x1, y2, x2, y2: <int>


        ---> <Menu>
        ______________________________________________________________________

        Refreshes a mini menu made of buttons of the keys of the action to show.
        It then returns it, to be assigned elsewhere.
        """
        changeable_keys = [f"Change {key}" for key in files.list_repeated_keys(self.action_to_show, files.map_keys())] + ["Add Key"]

        return objects.Menu(changeable_keys, (x1, y1, x2, y2), is_sub=True)

    def level_up(self, how_much=1):
        """
        ______________________________________________________________________

        how_much: <int>


        ---> None
        ______________________________________________________________________

        Increments by 'how_much' the level of the game.
        """
        self.game_level += how_much
        self.level_dict = files.map_level(self.game_level)

    def power_up(self, how_much=1):
        """
        ______________________________________________________________________

        how_much: <int>


        ---> None
        ______________________________________________________________________

        Increments by 'how_much' the power of the player.
        """
        self.power_level += how_much
        self.shooting_cooldown.initial_time = self.cool_cons // self.power_level

    def shoot_bullets(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Shoots bullets from player.
        """
        player_center_x = self.player.center()[0]

        if self.power_level  == 1:

            self.bullets.append(objects.Bullet(player_center_x - 5, self.player.y1 + 30, player_center_x + 5, self.player.y1 + 20,
                                how_hard=self.player.hardness, speed=2))

        elif self.power_level == 2:

            self.bullets.append(objects.Bullet(player_center_x - 5, self.player.y1 + 30, player_center_x + 5, self.player.y1 + 20,
                                how_hard=self.player.hardness, speed=3, bullet_type='sinusoidal_simple', first_to_right=True))

    def exec_bul_trajectory(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

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

            if bullet.y2 < -100 or bullet.has_no_health():

                self.bullets.remove(bullet)

            bullet.trajectory()

    def exec_enem_trajectory(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Moves each enemy according to its defined behaviour.
        """
        for enem in self.enemies:
            
            if enem.collides_with(self.player):

                if self.invulnerability.is_zero_or_less():

                    self.player.hp -= enem.hardness
                    self.invulnerability.reset()

            if enem.has_no_health() or enem.y1 > files.EXT_CONST["HEIGHT"] + 100:

                self.enemies.remove(enem)

            enem.trajectory()

    def exec_lvl_script(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Reads the level dictionary timeline and executes the instructions detailed within.
        """
        for instant in self.level_dict:

            if int(instant) == self.level_timer.current_time:

                for action in self.level_dict[instant]:

                    self.enemies.append(objects.Enemy(action['x1'], action['y1'], action['x2'], action['y2'], action['type']))
                
                self.level_dict.pop(instant)
                break

    def clear_assets(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Clears all enemies and bullets in their lists once returned to the main menu.
        """
        self.enemies = list()
        self.bullets = list()

    def advance_game(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        This function is that one of a wrapper, and advances the state of the game.
        """
        if self.is_in_game:

            self.menu_in_display = None

            self.exec_bul_trajectory()
            self.exec_enem_trajectory()
            self.exec_lvl_script()

            self.refresh_timers()

        else:

            self.show_debug_info = False

            if not self.menu_in_display.press_cooldown.is_zero_or_less():

                self.menu_in_display.press_cooldown.deduct(1)

    def refresh_timers(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Refreshes all the timers of the game, so that it updates theirs values.
        """
        if not self.level_timer.is_zero_or_less():

            self.level_timer.deduct(1)

        if not self.shooting_cooldown.is_zero_or_less():

            self.shooting_cooldown.deduct(1)

        if not self.debug_cooldown.is_zero_or_less():

            self.debug_cooldown.deduct(1)

        if not self.invulnerability.is_zero_or_less():

            self.invulnerability.deduct(1)

    def change_is_in_game(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Changes 'self.is_in_game' to its opposite.
        """
        self.is_in_game = not self.is_in_game

    def exit_game(self):
        """
        ______________________________________________________________________

        ---> None
        ______________________________________________________________________

        Sets the control variable 'self.exit' to 'True' to exit the game.
        """
        self.exit = True