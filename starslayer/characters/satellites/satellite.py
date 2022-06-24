"""
Player Satellite Companion Module.
"""

from typing import TYPE_CHECKING, Optional

from ...entity import Entity
from ...utils import HitCircle

if TYPE_CHECKING:
    from ...utils import BoundingShape


class Satellite(Entity, HitCircle):
    """
    A satellite companion.
    """

    def __init__(self,
                 cx: float,
                 cy: float,
                 radius: float,
                 orbit_center: "BoundingShape",
                 health: int=1,
                 how_hard: int=0,
                 texture_path: Optional[str]=None,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'Satellite'.
        """

        super().__init__(cx=cx,
                         cy=cy,
                         radius=radius,
                         health=health,
                         how_hard=how_hard,
                         can_spawn_outside=True,
                         texture_path=texture_path,
                         **kwargs)

        self.orbit_center: "BoundingShape" = orbit_center
        self.orbit_radius: float = self.distance_to(self.orbit_center)
        self.angle: float = self.orbit_center.angle_towards(self) # in radians


    def rotate(self, how_much: float) -> None:
        """
        Rotates the satellite across the orbit.

        if `how_much` is a positive value it rotates anti-clockwise,
        otherwise it rotates clockwise.
        """

        self.angle += how_much
        self.move_orbit(self.orbit_center,
                        self.angle,
                        self.orbit_radius)
