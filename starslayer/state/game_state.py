"""
Logics Module. Its purpose is to control the logic behaviour
of the game.
"""

from typing import List, Optional

from starslayer.scene.profilescene import ProfileScene

from ..bullets import Bullet, BulletNormalAcc, BulletSinusoidalSimple
from ..characters import Entity
from ..consts import (EXITING_DELAY, HEIGHT, KEYS_PATH, PLAYER_DAMAGED_SPRITE,
                      PLAYER_SPRITE, PROFILES_PATH, WIDTH)
from ..enemies import Enemy
from ..files import (LevelDict, ProfilesDict, StrDict, list_actions,
                     list_profiles, list_repeated_keys, load_json, map_level)
from ..hooks import HooksGroup
from ..hooks.groups import Menus
from ..hooks.groups import Miscellaneous as Misc
from ..hooks.groups import Movements
from ..logger import GameLogger
from ..scene import (ControlScene, InGameScene, MainScene, OptionScene, Scene,
                     SceneDict)
from ..selector import ColorSelector
from ..utils import Menu, Timer

CornersTuple = tuple[int | float, int | float, int | float, int | float]
TimerDict = dict[str, Timer]


class Game:
    """
    Class for the Game itself.
    """

    def __init__(self, *_args, **kwargs) -> None:
        """
        Initalizes an instance of type 'Game'.
        """

        # Level Parameters
        self.game_level: int = 1
        self.level_dict: LevelDict = map_level(1)

        # Player Parameters
        self.player: Entity = Entity(x1=(WIDTH // 2) - 30,
                                 y1=int(HEIGHT / 1.17) - 30,
                                 x2=(WIDTH // 2) + 30,
                                 y2=int(HEIGHT / 1.17) + 30,
                                 how_hard=1,
                                 speed=5,
                                 texture_path=(PLAYER_SPRITE, PLAYER_DAMAGED_SPRITE))
        self.power_level: int = kwargs.get("initial_power", 1)

        # Color Profiles
        self.color_profiles: ProfilesDict = load_json(PROFILES_PATH)
        self._color_theme: List[str] = list_profiles(self.color_profiles)[0]
        self.color_profile: StrDict = self.color_profiles[self._color_theme]

        # Sub-menu related
        self.action_to_show: str = list_actions(load_json(KEYS_PATH))[0]
        self.sub_menu: Optional[Menu] = None

        # Timers
        self.cool_cons: int = kwargs.get("cooldown_constant", 30)
        self.timers: TimerDict = {"invulnerability": Timer(50 + (self.power_level * 5)),
                                  "shooting_cooldown": Timer(self.cool_cons // self.power_level),
                                  "debug_cooldown": Timer(20),
                                  "level_timer": Timer(int(self.level_dict.pop("total_time")))}
        self.special_timers: TimerDict = {"exiting_cooldown": Timer(EXITING_DELAY)}

        # Enemies, Misc
        self.enemies: List[Enemy] = []
        self.bullets: List[Bullet] = []

        # Control Attributes
        self.is_on_prompt: bool = False
        # self.is_in_game: bool = False
        self.show_debug_info: bool = False
        self.show_about: bool = False
        self.is_on_prompt: bool = False
        self.exiting: bool = False
        self.exit: bool = False

        # Selector
        self.color_selector = self.generate_color_selector()
        self.attribute_to_edit: Optional[str] = None

        # Actions
        self.__hooks_groups: List[HooksGroup] = []
        self.add_group(Movements(self))
        self.add_group(Menus(self))
        self.add_group(Misc(self))

        # Scenes Related
        self.scenes: SceneDict = {}
        self.current_scene: Optional[Scene] = None

        mainscene = MainScene()
        optionscene = OptionScene(parent=mainscene)
        controlscene = ControlScene(parent=optionscene)
        profilescene = ProfileScene(parent=optionscene)
        ingamescene = InGameScene(parent=mainscene)
        self.add_scene(mainscene)
        self.add_scene(optionscene)
        self.add_scene(controlscene)
        self.add_scene(profilescene)
        self.add_scene(ingamescene)


    @staticmethod
    def process_key(key: str) -> str:
        """
        Reads which key was pressed, and returns its corresponding action.
        The key is guaranteed to already exist it the json file.
        """

        return load_json(KEYS_PATH).get(key)


    def add_group(self, new_group: HooksGroup) -> None:
        """
        Adds new group to internal actions groups list.
        """

        self.__hooks_groups.append(new_group)


    def delete_group(self, group: HooksGroup) -> Optional[HooksGroup]:
        """
        Deletes an action group.
        If it finds it, it returns such group.
        """

        group_to_return = None

        if group in self.__hooks_groups:

            group_to_return = group
            self.__hooks_groups.remove(group)

        return group_to_return


    def add_scene(self, new_scene: Scene) -> None:
        """
        Adds a new scene to the game.
        """

        if not self.current_scene:
            self.current_scene = new_scene

        self.scenes[new_scene.id] = new_scene
        new_scene.resfresh_sub_menus(self) # One initial refresh


    def remove_scene(self, scene: Scene) -> Optional[Scene]:
        """
        Removes and returns a scene of the game, if available.
        """

        if self.current_scene == scene:
            self.current_scene = None

        return self.scenes.pop(scene.id, None)


    def change_scene(self, scene_id: str) -> None:
        """
        Searches for a scene name id. If it finds it,
        the current scene is replaced.
        """

        scene = self.scenes.get(scene_id, None)

        if scene:

            self.current_scene = scene


    def execute_action(self, action: str) -> None:
        """
        Executes one specified action.
        """

        for group in self.__hooks_groups:

            group.execute_act(action)


    # pylint: disable=invalid-name
    def execute_button(self, x: int, y: int) -> None:
        """
        Tries to execute a button handler.
        """

        if self.current_scene and self.current_scene.execute_button(self, x, y):
            # There should be only one button in all of the
            # scenes that coincides with these coords
            return


    @property
    def log(self) -> GameLogger:
        """
        Returns the game logger.
        """

        return GameLogger()


    @property
    def is_in_game(self) -> bool:
        """
        Checks if the game is the playable area or not.
        """

        return self.current_scene == self.scenes.get("scene-in-game", "-= not-in-game =-")


    @property
    def invulnerability(self) -> Timer:
        """
        Returns the invulnerability the player has,
        after it has received damage.
        """

        return self.timers.get("invulnerability")


    @property
    def shooting_cooldown(self) -> Timer:
        """
        Returns the cooldown to shoot again.
        """

        return self.timers.get("shooting_cooldown")


    @property
    def debug_cooldown(self) -> Timer:
        """
        Returns the cooldown for showing debug messages.
        """

        return self.timers.get("debug_cooldown")


    @property
    def level_timer(self) -> Timer:
        """
        Returns the timer of the current level.
        """

        return self.timers.get("level_timer")


    @property
    def exiting_cooldown(self) -> Timer:
        """
        Returns the timer fot exiting the game.
        """

        return self.special_timers.get("exiting_cooldown")


    @property
    def selected_theme(self) -> str:
        """
        Returns the current color theme (name only).
        """

        return self._color_theme


    @selected_theme.setter
    def selected_theme(self, new_value: str) -> None:
        """
        If the selected theme changes, then the profile should also do it.
        """

        real_name = '_'.join(new_value.upper().split())

        if real_name in self.color_profiles:

            self._color_theme = real_name
            self.color_profile = self.color_profiles[real_name]


    def check_scene(self, name_id: str) -> bool:
        """
        Checks if a given scene is present in the game and is the
        current one showing.
        """

        return (name_id in self.scenes) and (self.current_scene == self.scenes[name_id])


    def go_prompt(self) -> None:
        """
        Sets the 'is_on_prompt' attribute to 'True' so that the
        next iteration, the program prompts the user for interaction.
        """

        self.is_on_prompt = True


    def prompt(self, *args, **kwargs) -> None:
        """
        Processes the action to prompt the user.
        """

        kwargs.update({"game": self})
        self.current_scene.prompt(*args, **kwargs)


    def generate_color_selector(self) -> ColorSelector:
        """
        Generates and assigns the color selector of the game.
        """

        aux_x = (WIDTH // 75)
        aux_y = (HEIGHT // 70)

        area_x1, area_y1, area_x2, area_y2 = ((WIDTH // 15),
                                              (HEIGHT * 0.065714),
                                              (WIDTH * 0.866666),
                                              (HEIGHT * 0.928571))
        palette_corners = (area_x1 + aux_x,
                           area_y1 + aux_y,
                           area_x2 - aux_x,
                           area_y1 + ((area_y2 - area_y1) / 2))
        color_selector: ColorSelector = ColorSelector(area=(area_x1, area_y1, area_x2, area_y2),
                                                      palette_area=palette_corners,
                                                      rows=20, cols=30)

        return color_selector


    def level_up(self, how_much: int=1) -> None:
        """
        Increments by 'how_much' the level of the game.
        """

        self.game_level += how_much
        self.level_dict = map_level(self.game_level)
        self.level_timer = Timer(int(self.level_dict.pop("total_time")))


    def power_up(self, how_much: int=1) -> None:
        """
        Increments by 'how_much' the power of the player.
        """

        self.power_level += how_much
        self.shooting_cooldown.initial_time = self.cool_cons // self.power_level


    def shoot_bullets(self) -> None:
        """
        Shoots bullets from player.
        """

        player_center_x = self.player.center[0]

        match self.power_level:

            case 1:

                self.bullets.append(BulletNormalAcc(x1=player_center_x - 5,
                                                    y1=self.player.y1 + 30,
                                                    x2=player_center_x + 5,
                                                    y2=self.player.y1 + 20,
                                                    how_hard=self.player.hardness,
                                                    speed=2))

            case 2:

                self.bullets.append(BulletSinusoidalSimple(x1=player_center_x - 5,
                                                           y1=self.player.y1 + 30,
                                                           x2=player_center_x + 5,
                                                           y2=self.player.y1 + 20,
                                                           how_hard=self.player.hardness,
                                                           speed=3,
                                                           first_to_right=True))

            case 3:

                self.bullets.append(BulletSinusoidalSimple(x1=player_center_x - 15,
                                                           y1=self.player.y1 + 30,
                                                           x2=player_center_x -5,
                                                           y2=self.player.y1 + 20,
                                                           how_hard=self.player.hardness,
                                                           speed=3,
                                                           first_to_right=True))
                self.bullets.append(BulletSinusoidalSimple(x1=player_center_x + 5,
                                                           y1=self.player.y1 + 30,
                                                           x2=player_center_x + 15,
                                                           y2=self.player.y1 + 20,
                                                           how_hard=self.player.hardness,
                                                           speed=3,
                                                           first_to_right=False))


    def exec_bul_trajectory(self) -> None:
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

            if bullet.y2 < -100 or bullet.has_no_health():

                self.bullets.remove(bullet)

            bullet.trajectory()


    def exec_enem_trajectory(self) -> None:
        """
        Moves each enemy according to its defined behaviour.
        """

        for enem in self.enemies:

            if enem.collides_with(self.player):

                if self.invulnerability.is_zero_or_less():

                    self.player.hp -= enem.hardness
                    self.invulnerability.reset()

            if enem.has_no_health() or enem.y1 > (HEIGHT * 1.15):

                self.enemies.remove(enem)

            enem.trajectory()


    def exec_lvl_script(self) -> None:
        """
        Reads the level dictionary timeline and executes the instructions detailed within.
        """

        for instant in self.level_dict:

            if int(instant) == self.level_timer.current_time:

                current_instant = self.level_dict.pop(instant)

                for action in current_instant:

                    enemy_type_to_add = Enemy.types[action["type"]] or Enemy.default

                    self.enemies.append(enemy_type_to_add(x1=int(action["x1"]),
                                                          y1=int(action["y1"]),
                                                          x2=int(action["x2"]),
                                                          y2=int(action["y2"])))

                break


    def clear_assets(self) -> None:
        """
        Clears all enemies and bullets in their lists once returned to the main menu.
        """

        self.enemies = []
        self.bullets = []


    def advance_game(self, keys_dict: dict[str, bool]) -> None:
        """
        This function is that one of a wrapper, and advances the state of the game.
        It takes a dictionary of the keys pressed to decide if it counts some timers.
        """

        self.refresh_return_timer(keys_dict)

        if self.is_in_game:

            self.exec_bul_trajectory()
            self.exec_enem_trajectory()
            self.exec_lvl_script()

            self.refresh_timers()

        else:

            self.show_debug_info = False
            self.current_scene.press_cooldown.count(1)


    def refresh_timers(self) -> None:
        """
        Refreshes all the in-game timers of the game, so that it updates theirs values.
        """

        for timer in self.timers.values():

            timer.count(1)


    def reset_timers(self) -> None:
        """
        Resets all the in-game timers of the game.
        """

        for timer in self.timers.values():

            timer.reset()


    def refresh_return_timer(self, keys_dict: dict[str, bool]) -> None:
        """
        Refreshes the return timer.
        """

        exit_correct_keys = list_repeated_keys("EXIT", load_json(KEYS_PATH))

        if any(keys_dict.get(key, False) for key in exit_correct_keys):

            self.exiting = True
            self.exiting_cooldown.deduct(1 if self.is_in_game else 2)

        else:

            self.exiting = False
            self.exiting_cooldown.reset()


    def change_is_in_game(self) -> None:
        """
        Changes 'self.is_in_game' to its opposite.
        """

        self.is_in_game = not self.is_in_game
