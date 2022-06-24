"""
Playable Character Module.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generator, List, Optional

from ..consts import HEIGHT, WIDTH
from ..entity import Entity
from ..power_levels import SimplePower
from ..sprites import Sprite
from ..utils import HitBox, Timer

if TYPE_CHECKING:
    from ..bullets import Bullet
    from ..power_levels import PowerLevel
    from ..state import Game
    from .satellites import Satellite


class PlayableCharacter(Entity, HitBox, ABC):
    """
    Abstract class for defining a playable character.
    """

    def __init__(self,
                 *,
                 has_satellite: bool=False,
                 satellite_type: Optional["Satellite"]=None,
                 sat_x: Optional[float]=None,
                 sat_y: Optional[float]=None,
                 sat_rad: Optional[float]=None,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'PlayableCharacter'.
        """

        super().__init__(**kwargs)

        if has_satellite and any((sat_x is None,
                                  sat_y is None,
                                  sat_rad is None,
                                  satellite_type is None)):
            raise ValueError("If the character has a shield, then its properties must be present.")

        self.base_speed: int = self.speed
        self.base_hardness: int = self.hardness
        self.power_level: "PowerLevel" = SimplePower()
        self.shooting_cooldown: Timer = Timer(self.power_level.cooldown)
        self.invulnerability: Timer = Timer(self.power_level.invulnerability)

        self.base_hp: int = self.max_hp
        self.can_upgrade: bool = False
        self.times_upgraded: int = 0
        self.ability_gauge: int = 0
        self._time_awareness: int = 1 # The higher, the slower the surroundings
        self.can_change_awareness: bool = True
        self.satellite: Optional["Satellite"] = (None
                                                 if not has_satellite
                                                 else satellite_type(cx=sat_x,
                                                                     cy=sat_y,
                                                                     radius=sat_rad,
                                                                     orbit_center=self))
        self.base_sprite: Sprite = self.sprite
        self.damaged_sprite_path: str = (f"{self.sprite_path}_damaged"
                                         if self.sprite_path is not None
                                         else None)
        self.damaged_sprite: Sprite = (Sprite(self.damaged_sprite_path)
                                       if self.damaged_sprite_path
                                       else None)


    @property
    def time_awareness(self) -> int:
        """
        Returns the time awareness of the character.
        """

        return self._time_awareness


    @time_awareness.setter
    def time_awareness(self, new_value: int) -> None:
        """
        Sets the time awareness, if possible.
        """

        if self.can_change_awareness:
            self._time_awareness = new_value


    def power_up(self) -> None:
        """
        Increments by the power of the playable character.
        """

        next_level = self.power_level.next_level()
        if next_level is not None:
            self.power_level = next_level

        self.change_cooldown(self.power_level.cooldown)
        self.change_invulnerability(self.power_level.invulnerability)


    def change_cooldown(self, new_cooldown: int) -> None:
        """
        Changes the shooting cooldown, for example when it
        powers up.
        """

        self.shooting_cooldown = Timer(new_cooldown)


    def change_invulnerability(self, new_invulnerability: int) -> None:
        """
        Changes the shooting invulnerability, for example when it
        powers up.
        """

        self.invulnerability = Timer(new_invulnerability)


    def get_timers(self) -> Generator[Timer, None, None]:
        """
        Yields each timer that the player has.
        """

        yield self.shooting_cooldown
        yield self.invulnerability


    def add_ability_points(self, points: int) -> None:
        """
        Adds the points to the ability gauge, if it isn't
        already at the max value.
        """

        if points < 0:
            raise ValueError(f"{points} is not a valid points value. " +
                             "It must be a positive integer or zero.")

        self.ability_gauge += points
        self.ability_gauge = min(self.ability_gauge, self.ability_threshold)


    def deduct_ability_points(self, points: int) -> None:
        """
        Deducts the points to the ability gauge, if it isn't
        already at the max value.
        """

        if points < 0:
            raise ValueError(f"{points} is not a valid points value. " +
                             "It must be a positive integer or zero.")

        self.ability_gauge -= points
        self.ability_gauge = max(self.ability_gauge, 0)


    def change_ability_gauge_percentage(self, percent: float) -> None:
        """
        Adds or deducts points to the gauge based on percentage,
        which must be in the range (0.0, 100.0].
        """

        if percent <= 0 or percent > 100:
            raise ValueError("percent value must be between (0.0, 100.0].")

        used_percentage = percent - self.ability_percentage()

        if used_percentage == 0:
            return

        points = (abs(used_percentage) / 100) * self.ability_threshold

        if used_percentage > 0:
            self.add_ability_points(points)

        else:
            self.deduct_ability_points(points)


    def reset_ability_points(self) -> None:
        """
        Resets the ability points back to its initial value.
        """

        self.ability_gauge = 0


    def can_use_ability(self) -> bool:
        """
        Checks if the player can use its ability.
        """

        return self.ability_gauge == self.ability_threshold


    def ability_percentage(self) -> float:
        """
        Returns the completion percentage of the ability gauge.
        """

        return (self.ability_gauge / self.ability_threshold) * 100


    def check_damaged_sprite(self) -> None:
        """
        If damaged, shows the damaged sprite accordingly.
        """

        if not self.invulnerability.time_is_up():
            self.sprite = self.damaged_sprite
            return

        self.sprite = self.base_sprite


    def refresh_hook(self) -> None:
        """
        Executes all internal actions that may be necessary for
        the character to be update with each iteration.

        Must be inherited to be useful.
        """

        return None


    @property
    @abstractmethod
    def ability_threshold(self) -> int:
        """
        The amount of points one must collect to be able
        to activate the player's ability.
        """

        raise NotImplementedError


    @property
    def bul_aux_y(self) -> float:
        """
        An auxiliar helper for calculating bullet output.
        """

        return HEIGHT / 28


    @property
    def bul_rad_aux(self) -> float:
        """
        An auxiliar helper for calculating bullet radius.
        """

        return WIDTH / 150


    @abstractmethod
    def ability_effect(self, game: "Game") -> None:
        """
        Applies the effect of the ability.
        """

        raise NotImplementedError


    @abstractmethod
    def shoot_simple_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots simple bullets.
        """

        raise NotImplementedError


    @abstractmethod
    def shoot_super_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots super bullets.
        """

        raise NotImplementedError


    @abstractmethod
    def shoot_ultra_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots ultra bullets.
        """

        raise NotImplementedError


    @abstractmethod
    def shoot_mega_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots mega bullets.
        """

        raise NotImplementedError


    @abstractmethod
    def shoot_hyper_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots hyper bullets.
        """

        raise NotImplementedError


    def move(self, dx: int, dy: int, freely: bool=False) -> bool:
        """
        Moves the chracter around inside the boundaries of the screen,
        along with its shield.
        """

        did_move = super().move(dx, dy, freely=freely)

        if self.satellite and did_move:
            self.satellite.move(dx, dy, freely=True)

        return did_move
