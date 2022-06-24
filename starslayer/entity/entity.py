"""
Characters Module. For storing playable characters
(mainly the player).
"""

from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from ..state import Game

ShipVariable = Optional[float | int | str]
EntityDict = Dict[str, ShipVariable]


class Entity:
    """
    Class for defining an entity.
    An entity is a hitbox with health, speed and other
    extra attributes.
    """

    def __init__(self,
                 *,
                 health: int=100,
                 how_hard: int=0,
                 speed: int=1,
                 ethereal: bool=False,
                  **kwargs: EntityDict) -> None:
        """
        Initializes an instance of type 'Entity'.

        Kwargs:

        `max_hp` is the maximum health points to be had.
        `how_hard` is the defence stat.
        `speed` is the speed of the entity movement.
        `ethereal` is if it should receive damage on impact.
        """

        # This here works only if Entity is before a bounding shape in the MRO
        super().__init__(**kwargs)

        self.max_hp: int = health
        self._hp: int = self.max_hp #pylint: disable=invalid-name
        self.hardness: int = how_hard
        self.speed: int = speed
        self.is_ethereal: bool = ethereal


    def __str__(self) -> str:
        """
        Returns a string with class information so it can be printed later.
        """

        return (f"health: {self.hp} - " +
                f"hardness: {self.hardness} - speed: {self.speed}")


    def __repr__(self) -> str:
        """
        Returns a string with class information so it can be parsed 'as is' later.
        """

        return str(self)


    @property
    def points_worth(self) -> int:
        """
        How many points should this enemy be worth at dying.
        This property should be overriden to be useful.
        """

        return 0


    @property
    # pylint: disable=invalid-name
    def hp(self) -> int:
        """
        Returns the current health points.
        """

        return self._hp


    # pylint: disable=invalid-name
    @hp.setter
    def hp(self, new_hp: int) -> None:
        """
        Sets the new health points.
        """

        if new_hp < 0:
            self._hp = 0
            return

        if new_hp > self.max_hp:
            self._hp = self.max_hp
            return

        self._hp = new_hp


    def die(self) -> None:
        """
        Drops the health points to zero.
        """

        self.hp = 0


    def is_dead(self) -> bool:
        """
        Returns 'True' if if the ship has 0 health points or less, and 'False' otherwise.
        """

        return self.hp <= 0


    def death_effect(self, _game: "Game") -> None:
        """
        Executes an given effect on the game, when the entity dies.

        This may be inherited to be useful.
        """

        return None


    def health_percentage(self) -> float:
        """
        Calculates the percentage of the remaining health.
        """

        return (self.hp / self.max_hp) * 100


    def take_damage(self, how_much: int) -> int:
        """
        Process damage taken.
        Returns the remaining health
        """

        if not self.is_ethereal:
            self.hp -= how_much

        if self.hp < 0:
            self.die()

        return self.hp
