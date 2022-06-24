"""
Player Shield Module.
"""

from typing import TYPE_CHECKING

from ...consts import SHIELD_REL_PATH
from .satellite import Satellite

if TYPE_CHECKING:
    from ...utils import BoundingShape


class Shield(Satellite):
    """
    Shield for a player.
    """

    def __init__(self,
                 cx: float,
                 cy: float,
                 radius: float,
                 orbit_center: "BoundingShape",
                 **kwargs) -> None:
        """
        Initializes an instance of type 'Shield'.
        """

        super().__init__(cx=cx,
                         cy=cy,
                         radius=radius,
                         health=1000000,
                         how_hard=5, # But no cooldown
                         texture_path=SHIELD_REL_PATH,
                         orbit_center=orbit_center,
                         **kwargs)
