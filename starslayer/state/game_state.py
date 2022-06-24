#pylint: disable=too-many-lines
"""
Logics Module. Its purpose is to control the logic behaviour
of the game.
"""

from importlib import import_module
from math import ceil
from os import listdir
from random import choices, randrange
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

from ..consts import (ACTIONS_PATH, EXITING_DELAY, HEIGHT, HOOKS_GROUPS_PATH,
                      PLAYABLE_WIDTH, PLAYER_HEALTH_BAR_ANIM, PROFILES_PATH,
                      SCORES_PATH, SFX_SHOOT, WIDTH)
from ..drops import DropsList
from ..enemies import EnemyCommonA, EnemyCommonB, EnemySwift
from ..files import (ProfilesDict, StrDict, dump_json, get_action_from_key,
                     list_action_keys, list_actions, list_profiles, load_json)
from ..gamelib import EventType
from ..gamelib import play_sound as lib_play_sound
from ..hooks import HooksGroup
from ..logger import GameLogger
from ..scene import (AboutScene, CharacterScene, ControlScene, GameOverScene,
                     InGameScene, MainScene, OptionScene, ProfileScene, Scene,
                     SceneDict, ScoreBoardScene)
from ..selector import ColorSelector
from ..utils import Chronometer, HitBox, HitCircle, Menu, Timer

if TYPE_CHECKING:
    from ..bullets import Bullet
    from ..characters import PlayableCharacter
    from ..enemies import Enemy
    from ..entity import Entity
    from ..gamelib import Event
    from ..utils import BoundingShape

CornersTuple = tuple[int | float, int | float, int | float, int | float]
TimerDict = Dict[str, Timer]
ChronDict = Dict[str, Chronometer]
EventsDict = Dict[str, bool]
BulletsList = List["Bullet"]
ScoreBoard = List[List[str | int]]


class Game:
    """
    Class for the Game itself.
    """

    def __init__(self) -> None:
        """
        Initalizes an instance of type 'Game'.
        """

        # Level Parameters
        self.game_level: int = 1
        self.score: int = 0

        # Upgrade/Evolvutions
        self.times_upgraded: int = 0
        self.max_upgrade_level = 4
        self.thresholds: List[int] = [2500, 5000, 10000, 20000]
        if len(self.thresholds) != self.max_upgrade_level:
            raise ValueError(f"Thresholds length {len(self.thresholds)} does not coincide " +
                             f"with max upgrade level {self.max_upgrade_level}")

        # Player Parameters
        self.player: Optional["PlayableCharacter"] = None
        self.player_bullets: BulletsList = []

        # Color Profiles
        self.color_profiles: ProfilesDict = load_json(PROFILES_PATH)
        self._color_theme: List[str] = list_profiles(self.color_profiles)[0]
        self.color_profile: StrDict = self.color_profiles[self._color_theme]

        # Sub-menu related
        self.action_to_show: str = list_actions(load_json(ACTIONS_PATH))[0]
        self.sub_menu: Optional[Menu] = None

        # Timers
        self.timers: TimerDict = {"debug_cooldown": Timer(20)}
        self.special_timers: TimerDict = {"exiting_cooldown": Timer(EXITING_DELAY)}
        self.chronometers: ChronDict = {"real_time": Chronometer()}

        # Enemies
        self.enemies: List["Enemy"] = []
        self.enemies_bullets: BulletsList = []

        # Drops
        self.drops: DropsList = []

        # Control Attributes
        self.control_attributes: Dict[str, bool] = {}
        self.control_attributes.update(is_on_prompt=False,
                                       show_debug_info=False,
                                       exiting=False,
                                       exit=False,
                                       used_cheats=False,
                                       has_audio=True)

        # Selector
        self.color_selector = self.generate_color_selector()
        self.attribute_to_edit: Optional[str] = None

        # Actions
        self.__hooks_groups: List[HooksGroup] = []
        self.load_hook_groups()

        # Scenes
        self.scenes: SceneDict = {}
        self.current_scene: Optional[Scene] = None
        self.load_scenes()

        # Events control
        self.keys_pressed: EventsDict = {}
        self.keys_released: EventsDict = {}
        self.events_processed: EventsDict = {}
        self.time_flow: int = 60 # fps

        # Combinations
        self.typing_cooldown: Timer = Timer(15)
        self.combinations: List[str] = []


    @staticmethod
    def process_key(key: str) -> str:
        """
        Reads which key was pressed, and returns its corresponding action.
        The key is guaranteed to already exist it the json file.
        """

        return get_action_from_key(key, load_json(ACTIONS_PATH))


    def apply_events(self,
                     key: str,
                     events_dict: EventsDict,
                     action: str,
                     original_action: str) -> None:
        """
        Updates the events dictionaries to match the current events.
        """

        if events_dict.get(key, False):
            self.events_processed[action] = True

        elif all((not events_dict.get(repeated_key, False)
                 for repeated_key in list_action_keys(original_action,
                                                      load_json(ACTIONS_PATH)))):
            self.events_processed[action] = False


    def classify_events(self,
                        event: "Event",
                        cursor_coords: Dict[str, Optional[float]]) -> None:
        """
        Porperly updates some dictionaries and classifies the events
        for their later processing.
        """

        if event.type == EventType.KeyPress:
            self.keys_pressed[event.key] = True
            self.keys_released[event.key] = False
            self.combinations.append(event.key)
            self.typing_cooldown.reset()

        elif event.type == EventType.KeyRelease:
            self.keys_pressed[event.key] = False
            self.keys_released[event.key] = True

        elif event.type in (EventType.ButtonPress, EventType.ButtonRelease):
            self.execute_button(event.x, event.y,
                                event_type=event.type,
                                mouse_button=event.mouse_button)

        elif event.type == EventType.Motion:
            cursor_coords['x'] = event.x
            cursor_coords['y'] = event.y


    def process_events(self) -> None:
        """
        Processes all the events currently happening.
        """

        for key in self.keys_pressed:

            action = self.process_key(key)
            if action is None:
                continue
            self.apply_events(key, self.keys_pressed, action, action)

        for key_r in self.keys_released:

            original_action = self.process_key(key_r)
            if original_action is None:
                continue
            action = f"{original_action}_RELEASE"
            self.apply_events(key_r, self.keys_released, action, original_action)
            self.keys_released[key_r] = False # Release events should be done only once

        for game_action in self.events_processed:
            if self.events_processed.get(game_action, False):
                self.execute_action(game_action)

        if self.combinations:
            self.execute_combinations()


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


    def load_hook_groups(self) -> None:
        """
        Loads all the hook groups located in the `starlsayer.hooks.groups` package.
        """

        for file_name in listdir(HOOKS_GROUPS_PATH):
            if file_name.startswith("__"):
                continue

            module = import_module(f"..hooks.groups.{file_name.removesuffix('.py')}",
                                   "starslayer.state")
            module.setup_hook(self)


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

        if scene is not None:
            self.current_scene.reset_hook()
            self.current_scene = scene
            self.clear_assets()


    def load_scenes(self) -> None:
        """
        Loads the scenes into the game.
        """

        mainscene = MainScene()
        optionscene = OptionScene(parent=mainscene)
        controlscene = ControlScene(parent=optionscene)
        profilescene = ProfileScene(parent=optionscene)
        characterscene = CharacterScene(parent=mainscene)
        ingamescene = InGameScene(parent=mainscene)
        gameoverscene = GameOverScene(parent=mainscene)
        aboutscene = AboutScene(parent=mainscene)
        scoreboardscene = ScoreBoardScene(parent=mainscene)

        self.add_scene(mainscene)
        self.add_scene(optionscene)
        self.add_scene(controlscene)
        self.add_scene(profilescene)
        self.add_scene(characterscene)
        self.add_scene(ingamescene)
        self.add_scene(gameoverscene)
        self.add_scene(aboutscene)
        self.add_scene(scoreboardscene)


    def start_game(self) -> None:
        """
        Formally starts the game.
        """

        if not self.player:
            self.log.error(f"Player {self.player!r} is not a valid playable character.")
            return

        self.game_level = 1
        self.times_upgraded = 0
        self.real_time.reset()
        self.used_cheats = False
        self.score = 0
        self.change_scene("scene-in-game")
        self.change_menu_visibility(True)


    def end_game(self) -> None:
        """
        Realizes the procedures for ending a run.
        """

        self.show_debug_info = False
        self.change_scene("scene-gameover")


    def execute_action(self, action: str) -> None:
        """
        Executes one specified action.
        """

        for group in self.__hooks_groups:
            group.execute_act(action)


    # pylint: disable=invalid-name
    def execute_button(self, x: int, y: int, **kwargs) -> None:
        """
        Tries to execute a button handler.
        """

        if self.current_scene and self.current_scene.execute_button(self, x, y, **kwargs):
            # There should be only one button in all of the
            # scenes that coincides with these coords
            return


    def _format_combination(self, combination: List[str]) -> str:
        """
        Formats a list of characters into a readable combination.
        """

        combination = ''.join(self.combinations)
        replacements = {}
        replacements.update(space=' ',
                            minus='-',
                            plus='+',
                            Tab='\t',
                            Return='\n',
                            Caps_Lock='',
                            Up='↑',
                            Down='↓',
                            Left='←',
                            Right='→')

        for old, new in replacements.items():
            combination = combination.replace(old, new)

        return combination


    def execute_combinations(self) -> None:
        """
        Tries to execute all available combinations.
        """

        success = False
        comb_name = self._format_combination(self.combinations)

        for group in self.__hooks_groups:
            if group.execute_combination(comb_name):
                success = True

        if success:
            self.combinations.clear()


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
    def debug_cooldown(self) -> Timer:
        """
        Returns the cooldown for showing debug messages.
        """

        return self.timers.get("debug_cooldown")


    @property
    def real_time(self) -> Chronometer:
        """
        Returns the real time of the current game.
        """

        return self.chronometers.get("real_time")


    @property
    def exiting_cooldown(self) -> Timer:
        """
        Returns the timer fot exiting the game.
        """

        return self.special_timers.get("exiting_cooldown")


    @property
    def is_on_prompt(self) -> bool:
        """
        Returns the control boolean `is_on_prompt`.
        """

        return self.control_attributes.get("is_on_prompt")


    @is_on_prompt.setter
    def is_on_prompt(self, new_value: bool) -> None:
        """
        Changes the value for the control boolean `is_on_prompt`.
        """

        self.control_attributes["is_on_prompt"] = new_value


    @property
    def show_debug_info(self) -> bool:
        """
        Returns the control boolean `show_debug_info`.
        """

        return self.control_attributes.get("show_debug_info")


    @show_debug_info.setter
    def show_debug_info(self, new_value: bool) -> None:
        """
        Changes the value for the control boolean `show_debug_info`.
        """

        self.control_attributes["show_debug_info"] = new_value


    @property
    def exiting(self) -> bool:
        """
        Returns the control boolean `exiting`.
        """

        return self.control_attributes.get("exiting")


    @exiting.setter
    def exiting(self, new_value: bool) -> None:
        """
        Changes the value for the control boolean `exiting`.
        """

        self.control_attributes["exiting"] = new_value


    @property
    def exit(self) -> bool:
        """
        Returns the control boolean `exit`.
        """

        return self.control_attributes.get("exit")


    @exit.setter
    def exit(self, new_value: bool) -> None:
        """
        Changes the value for the control boolean `exit`.
        """

        self.control_attributes["exit"] = new_value


    @property
    def used_cheats(self) -> bool:
        """
        Returns the control boolean `used_cheats`.
        """

        return self.control_attributes.get("used_cheats")


    @used_cheats.setter
    def used_cheats(self, new_value: bool) -> None:
        """
        Changes the value for the control boolean `used_cheats`.
        """

        self.control_attributes["used_cheats"] = new_value


    @property
    def has_audio(self) -> bool:
        """
        Returns the control boolean `has_audio`.
        """

        return self.control_attributes.get("has_audio")


    @has_audio.setter
    def has_audio(self, new_value: bool) -> None:
        """
        Changes the value for the control boolean `has_audio`.
        """

        self.control_attributes["has_audio"] = new_value


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


    @property
    def all_bullets(self) -> BulletsList:
        """
        Returns all the bullets of the game.
        """

        return self.player_bullets + self.enemies_bullets


    @property
    def all_threats(self) -> List[Union["Enemy", "Bullet"]]:
        """
        Returns all the threats to the player.
        """

        return self.enemies + self.enemies_bullets


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

        kwargs.update(game=self)
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


    def add_score_to_board(self,
                           new_name: str,
                           new_power: str,
                           new_level: int,
                           new_score: int) -> None:
        """
        Adds a new score to the scoreboard.
        """

        scores: ScoreBoard = load_json(SCORES_PATH).get("scores", None)

        if scores is None:
            return

        scores.append([new_name, new_power, new_level, new_score])
        scores.sort(reverse=True, key=(lambda elem : elem[3])) # sort by its fourth element

        if len(scores) > 10:
            while len(scores) > 10:
                scores.pop() # Only ten values may exist at a time.


        dump_json({"scores": scores}, SCORES_PATH)


    def clear_scoreboard(self) -> None:
        """
        Empties the scoreboard.
        """

        dump_json({"scores": []}, SCORES_PATH)


    def change_menu_visibility(self, value: bool) -> None:
        """
        Changes the current scene menus to the
        preferred value.
        """

        for menu in self.current_scene.menus:
            menu.hidden = value


    def level_up(self, how_much: int=1) -> None:
        """
        Increments by 'how_much' the level of the game.
        """

        self.game_level += how_much


    def try_level_up(self) -> None:
        """
        Checks the correct conditions for leveling up.
        """

        each_points = 500
        is_over_threshold = self.score >= (self.game_level * each_points)

        if is_over_threshold:
            actual_level = (self.score // each_points) + 1
            self.level_up(actual_level - self.game_level)


    def can_upgrade(self) -> bool:
        """
        Checks if the game has yet to reach the maximum
        upgrade level.
        """

        return (self.times_upgraded < self.max_upgrade_level and
                self.score >= self.thresholds[self.times_upgraded])


    def try_upgrading(self) -> None:
        """
        Checks the correct conditions for prompting the user
        to upgrade or evolve.
        """

        if not self.can_upgrade():
            return

        self.change_menu_visibility(False)


    def upgrade_character(self) -> None:
        """
        Upgrades the player's properties.
        """

        coefficient = 1 + 0.1 * (self.times_upgraded + 1)

        self.player.speed =  ceil(self.player.speed * coefficient)
        self.player.hardness =  ceil(self.player.hardness * coefficient)

        self.times_upgraded += 1
        self.change_menu_visibility(True)


    def evolve_character(self) -> None:
        """
        Evolves the player's power level.
        """

        self.player.power_up()
        self.times_upgraded += 1

        self.change_menu_visibility(True)


    def shoot_bullets(self) -> None:
        """
        Shoots bullets from player.
        """

        self.player.power_level.shoot_bullets(self.player, self.player_bullets)
        self.play_sound(SFX_SHOOT)


    def play_sound(self, sound_path: str) -> None:
        """
        Plays a sound, if the game has audio.
        """

        if self.has_audio:
            lib_play_sound(sound_path)


    def is_time_flowing(self) -> bool:
        """
        For some elements in the screen, they should only move when it is right.
        """

        awareness = 1

        if self.player:
            awareness = self.player.time_awareness

        return self.real_time.current_time % awareness == 0


    def shape_is_out_bounds(self, shape: "BoundingShape") -> bool:
        """
        Checks if a shape is outside the boundaries of the screen.
        """

        return any((shape.is_over(-(HEIGHT * 0.15)),
                    shape.is_below(HEIGHT * 1.15),
                    shape.is_left_of(-(WIDTH * 0.2)),
                    shape.is_right_of(WIDTH * 1.2)))


    def check_shape_pos_and_entity_health(self,
                                          entity: Union["Entity", "BoundingShape"],
                                          container: List["Entity"]) -> bool:
        """
        Checks if an entity should disappear from the screen.

        Returns 'True' if the entity in question is dead, otherwise
        returns 'False'.
        """

        return self.check_entity_existence(entity,
                                           container,
                                           (self.shape_is_out_bounds(entity),
                                            entity.is_dead()))


    def check_shape_pos(self,
                        entity: Union["Entity", "BoundingShape"],
                        container: List["Entity"]) -> bool:
        """
        Checks if an shape should disappear from the screen.

        Returns 'True' if the entity in question is dead, otherwise
        returns 'False'.
        """

        return self.check_entity_existence(entity,
                                           container,
                                           (self.shape_is_out_bounds(entity),)) # comma needed


    def check_entity_existence(self,
                              entity: Union["Entity", "BoundingShape"],
                              container: List["Entity"],
                              checks: Tuple[bool, ...]) -> bool:
        """
        If any checks are set, the entity or shape is removed
        from the container.
        """

        if any(checks):
            try:
                container.remove(entity)
            except ValueError:
                pass

            return True

        return False


    def check_death_effects(self, threat: "Entity") -> None:
        """
        Tests if the threat is dead. If so, it harvests its points.
        """

        if not threat.is_dead():
            return

        self.score += threat.points_worth
        self.player.add_ability_points(threat.points_worth)


    def _check_collision_type(self,
                              threat: "BoundingShape",
                              defender: "BoundingShape") -> bool:
        """
        Checks which type of collision to test with another entity.
        """

        if isinstance(threat, HitBox):
            return defender.collides_with_box(threat)

        if isinstance(threat, HitCircle):
            return defender.collides_with_circle(threat)


    def update_health_anim(self) -> None:
        """
        Updates the health bar animations.
        """

        for health_bar_anim in self.current_scene.\
                                find_animation_match(fr"^{PLAYER_HEALTH_BAR_ANIM}_[0-9]+$"):
            health_bar_anim.change_crop(self.player.health_percentage())


    def check_damage_to_player(self,
                               threat: "Entity",
                               *,
                               reciprocal: bool=False) -> None:
        """
        Checks a collision of a threat with the player.

        Returns `True` if the player received damage, or
        `False` otherwise.
        """

        received_damage = False

        if not self._check_collision_type(threat, self.player):
            return received_damage

        if reciprocal:
            threat.take_damage(self.player.hardness)

        if self.player.invulnerability.time_is_up():
            self.player.take_damage(threat.hardness)
            self.player.invulnerability.reset()

            if reciprocal:
                threat.take_damage(self.player.hardness)

            received_damage = True
            self.update_health_anim()

        return received_damage


    def check_damage_to_shield(self,
                               threat: "Entity",
                               threat_container: List["Entity"],
                               *,
                               reciprocal: bool=True) -> None:
        """
        Checks a collision of a threat with the player's shield.

        Returns `True` if the shield received damage, or
        `False` otherwise.
        """

        received_damage = False

        shield = self.player.satellite
        if not shield:
            return

        if self._check_collision_type(threat, shield):
            shield.take_damage(threat.hardness)

            if reciprocal:
                threat.take_damage(shield.hardness)

            self.check_death_effects(threat)
            received_damage = True

        if self.is_time_flowing():
            self.check_shape_pos_and_entity_health(threat, threat_container)

        return received_damage


    def exec_player_bul_trajectory(self) -> None:
        """
        Moves each player bullet according to their trajectory.
        Player bullets do not actually hurt the player.
        """

        for player_bullet in self.player_bullets:
            player_bullet.trajectory()

            for threat in self.all_threats:
                if self._check_collision_type(threat, player_bullet):
                    threat.take_damage(player_bullet.hardness)
                    player_bullet.take_damage(threat.hardness)
                    self.check_death_effects(threat)

                    break

            self.check_shape_pos_and_entity_health(player_bullet, self.player_bullets)


    def exec_enem_trajectory(self) -> None:
        """
        Moves each enemy according to its defined behaviour.
        """

        for enem in self.enemies:
            self.check_damage_to_shield(enem, self.enemies)
            self.check_damage_to_player(enem)

            if not self.is_time_flowing():
                continue

            enem.trajectory()
            if self.check_shape_pos_and_entity_health(enem, self.enemies):
                enem.death_effect(self)
                enem.give_loot(self.drops)
            enem.try_shoot(self.enemies_bullets)


    def exec_enem_bul_trajectory(self) -> None:
        """
        Moves each player bullet according to their trajectory.
        These ones are the ones that do ouchie-ouchie.
        """

        for enem_bullet in self.enemies_bullets:
            self.check_damage_to_shield(enem_bullet, self.enemies_bullets)
            self.check_damage_to_player(enem_bullet, reciprocal=True)

            if self.is_time_flowing():
                enem_bullet.trajectory()
                self.check_shape_pos_and_entity_health(enem_bullet, self.enemies_bullets)


    def exec_drop_trajectory(self) -> None:
        """
        Moves each loot drop and checks collision with the player.
        """

        for drop in self.drops:
            if self._check_collision_type(drop, self.player):
                drop.effect(self)
                self.drops.remove(drop)

            drop.trajectory()
            self.check_shape_pos(drop, self.drops)


    def spawn_enemies(self,
                      *,
                      when: Optional[float]=None,
                      each: Optional[float]=None,
                      enemy_types: List["Enemy"],
                      weights: Optional[List[float]]=None,
                      amount_from: int=1,
                      amount_until: int=1,
                      width: int=(WIDTH // 25),
                      height: int=(HEIGHT // 23),
                      spacing_x: Optional[int]=None,
                      spacing_y: Optional[int]=None,
                      from_x: Optional[int]=None,
                      until_x: Optional[int]=None,
                      from_y: int=-50,
                      until_y: int=0,
                      disregard_timer_start: bool=False,
                      **gen_kwargs) -> None:
        """
        Given the parameters, effectively spawns the enemies on the game.
        """

        if when is None and each is None:
            raise TypeError("either 'when' or 'each' must be setted")

        if weights is not None and (len(weights) != len(enemy_types)):
            raise ValueError("If provided, the weights list must be of the same " +
                             "length than the enemy types.")

        if until_x is not None and until_x < width:
            raise ValueError("The are end should be before the very width of the sprite.")

        if any(((not self.real_time.current_time if not disregard_timer_start else False),
                (when is not None and self.real_time.current_time != when),
                (each is not None and self.real_time.current_time % each != 0),
                amount_from > amount_until)):
            return

        weights_used = weights or [1.0 for _ in enemy_types]

        spacing_x = spacing_x or width
        from_x = from_x or width
        until_x = until_x or (PLAYABLE_WIDTH - 2 * width)

        spacing_y = spacing_y or 5
        max_possible = until_x // (width + 1)

        if amount_until >= max_possible:
            amount_until = max_possible - 1

            if amount_until < amount_from:
                amount_from = amount_until

        number_of_enemies = randrange(amount_from, amount_until + 1) # +1 'cause it's not inclusive

        range_x = lambda : randrange(from_x, until_x, spacing_x)
        range_y = lambda : randrange(from_y, until_y, spacing_y)

        for _ in range(number_of_enemies):

            x1 = range_x()
            y1 = range_y()

            type_chosen = choices(enemy_types, weights_used)[0]
            if not type_chosen:
                continue

            new_enemy: "Enemy" = type_chosen(x1=x1,
                                             y1=y1,
                                             x2=x1 + width - 1,
                                             y2=y1 + height - 1,
                                             can_spawn_outside=True,
                                             **gen_kwargs)

            if any(new_enemy.collides_with_box(enemy)
                   for enemy in self.enemies):
                continue

            self.enemies.append(new_enemy)


    def generate_enemies(self) -> None:
        """
        Generates specific types on enemies depending on the
        current game level.
        """

        if not self.is_time_flowing():
            return

        weak_enemies = [EnemyCommonA, EnemyCommonB, EnemySwift, None]

        if self.game_level in range(1, 6): # level 1-5
            self.spawn_enemies(each=475,
                               enemy_types=weak_enemies,
                               weights=[60.0, 40.0, 0.0, 0.0],
                               amount_from=2,
                               amount_until=3,
                               disregard_timer_start=True)
            self.spawn_enemies(each=200,
                               enemy_types=weak_enemies,
                               weights=[0.0, 0.0, 20.0, 80.0],
                               amount_from=1,
                               amount_until=1,
                               until_x=WIDTH * 0.1,
                               # Gen Kwargs
                               homing_target=self.player)

        elif self.game_level in range(6, 11): # level 6-10
            self.spawn_enemies(each=350,
                               enemy_types=weak_enemies,
                               weights=[50.0, 50.0, 0.0, 0.0],
                               amount_from=4,
                               amount_until=6)
            self.spawn_enemies(each=175,
                               enemy_types=weak_enemies,
                               weights=[0.0, 0.0, 25.0, 75.0],
                               amount_from=1,
                               amount_until=2,
                               until_x=WIDTH * 0.1,
                               # Gen Kwargs
                               homing_target=self.player)

        elif self.game_level >= 11: # level 11-inf
            self.spawn_enemies(each=200,
                               enemy_types=weak_enemies,
                               weights=[50.0, 50.0, 0.0, 0.0],
                               amount_from=6,
                               amount_until=9)
            self.spawn_enemies(each=150,
                               enemy_types=weak_enemies,
                               weights=[0.0, 0.0, 40.0, 60.0],
                               amount_from=1,
                               amount_until=2,
                               until_x=WIDTH * 0.1,
                               # Gen Kwargs
                               homing_target=self.player)


    def clear_assets(self) -> None:
        """
        Clears all enemies and bullets in their lists once returned to the main menu.
        """

        self.enemies.clear()
        self.player_bullets.clear()
        self.enemies_bullets.clear()


    def advance_game(self) -> None:
        """
        This function is that one of a wrapper, and advances the state of the game.
        It takes a dictionary of the keys pressed to decide if it counts some timers.
        """

        self.refresh_exit_timer(self.keys_pressed)

        self.refresh_typing()
        self.current_scene.press_cooldown.count(1)
        self.current_scene.refresh_hook()

        if not self.is_in_game:
            return

        self.generate_enemies()
        self.exec_enem_trajectory()
        self.exec_enem_bul_trajectory()
        self.exec_player_bul_trajectory()
        self.exec_drop_trajectory()
        self.player.check_damaged_sprite()
        self.player.refresh_hook()

        self.try_level_up()
        self.try_upgrading()
        self.refresh_timers()

        if self.player.is_dead():
            self.end_game()


    def refresh_timers(self) -> None:
        """
        Refreshes all the in-game timers of the game, so that it updates theirs values.
        """

        for pl_timer in self.player.get_timers():
            pl_timer.count(1)

        for timer in self.timers.values():
            timer.count(1)

        for chrono in self.chronometers.values():
            chrono.count(1)

    def reset_timers(self) -> None:
        """
        Resets all the in-game timers of the game.
        """

        for timer in self.timers.values():
            timer.reset()

        for pl_timer in self.player.get_timers():
            pl_timer.reset()


    def refresh_typing(self) -> None:
        """
        Refreshes the typing cooldown for combinations.
        """

        self.typing_cooldown.count(1)
        if self.typing_cooldown.time_is_up():
            self.combinations.clear()


    def refresh_exit_timer(self, keys_dict: EventsDict) -> None:
        """
        Refreshes the exit timer.
        """

        exit_correct_keys = list_action_keys("EXIT", load_json(ACTIONS_PATH))

        if any(keys_dict.get(key, False) for key in exit_correct_keys):

            self.exiting = True
            self.exiting_cooldown.deduct(1 if self.is_in_game else 2)

        else:

            self.exiting = False
            self.exiting_cooldown.reset()
