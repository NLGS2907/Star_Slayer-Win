"""
Player Cannon Module.
"""

from typing import TYPE_CHECKING

from ...consts import CANNON_REL_PATH
from .satellite import Satellite

if TYPE_CHECKING:
    from ...utils import BoundingShape


class Cannon(Satellite):
    """
    Cannon for a player.
    """

    def __init__(self,
                 cx: float,
                 cy: float,
                 radius: float,
                 orbit_center: "BoundingShape",
                 **kwargs) -> None:
        """
        Initializes an instance of type 'Cannon'.
        """

        super().__init__(cx=cx,
                         cy=cy,
                         radius=radius,
                         health=10,
                         how_hard=0,
                         ethereal=True,
                         texture_path=CANNON_REL_PATH,
                         orbit_center=orbit_center,
                         **kwargs)
