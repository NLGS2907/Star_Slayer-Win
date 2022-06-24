"""
Viper Dodger character Module.
"""

from math import radians
from typing import TYPE_CHECKING, List, Optional

from starslayer.bullets.bullet_sprites_types import BulletSprites

from ..bullets import (BulletAccel, BulletElectric, BulletRadial,
                       BulletSinusoidalSimple)
from ..consts import HEIGHT, VIPER_DODGER_REL_PATH, WIDTH
from ..utils import Timer
from .playable_character import PlayableCharacter
from .satellites import Shield

if TYPE_CHECKING:
    from ..bullets import Bullet
    from ..state import Game
    from ..utils import BoundingShape


class ViperDodgerCharacter(PlayableCharacter):
    """
    The Viper Dodger playable character.

    Its special power resides in slowing time.
    """

    # pylint: disable=invalid-name
    def __init__(self,
                 *,
                 threats_pool: Optional[List["BoundingShape"]]=None,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'ViperDodgerCharacter'.
        """

        width_aux = WIDTH / 25
        height_aux = HEIGHT / (70 / 3)
        x1 = (WIDTH / 2) - width_aux
        y1 = (HEIGHT / 1.17) - height_aux
        x2 = (WIDTH / 2) + width_aux
        y2 = (HEIGHT / 1.17) + height_aux

        super().__init__(x1=x1,
                         y1=y1,
                         x2=x2,
                         y2=y2,
                         health=80,
                         how_hard=1,
                         speed=7,
                         texture_path=VIPER_DODGER_REL_PATH,
                         has_satellite=True,
                         satellite_type=Shield,
                         sat_x=x2 + width_aux,
                         sat_y=y1 - height_aux,
                         sat_rad=width_aux * 0.45,
                         **kwargs)

        self._to_right: bool = True
        self.ability_timer: Timer = Timer(500.0)
        self.ability_timer.drop()
        self.threats_pool: List["BoundingShape"] = ([] if threats_pool is None else threats_pool)


    @property
    def ability_threshold(self) -> int:
        """
        The amount of points one must collect to be able
        to activate the player's ability.
        """

        return 1000


    def ability_effect(self, game: "Game") -> None:
        """
        Applies the effect of the ability.
        """

        self.time_awareness = 5
        self.ability_timer.reset()
        self.reset_ability_points()


    def _is_using_ability(self) -> bool:
        """
        Wrapper for checking if the player activated the ability.
        """

        return not self.ability_timer.time_is_up()


    def _change_direction(self) -> None:
        """
        Alternates between shooting the bullet left or right.
        """

        self._to_right = not self._to_right


    def refresh_hook(self) -> None:
        """
        Updates the ability timer.
        """

        percentage = (self.ability_timer.current_time / self.ability_timer.base_time) * 100

        self.ability_timer.count(1.0)

        if self._is_using_ability():
            self.change_ability_gauge_percentage(percentage)
            return

        self.time_awareness = 1


    def shoot_simple_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots simple bullets.
        """

        center_x, center_y = self.center

        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=1,
                                              how_hard=self.hardness,
                                              speed=5,
                                              first_to_right=self._to_right))

        self._change_direction()


    def shoot_super_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots super bullets.
        """

        center_x, center_y = self.center

        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=1,
                                              how_hard=self.hardness,
                                              speed=5.5,
                                              amplitude=15.0,
                                              first_to_right=False))
        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=2,
                                              how_hard=self.hardness,
                                              speed=4.5,
                                              first_to_right=False))
        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=2,
                                              how_hard=self.hardness,
                                              speed=4.5,
                                              first_to_right=True))
        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=1,
                                              how_hard=self.hardness,
                                              speed=5.5,
                                              amplitude=15.0,
                                              first_to_right=True))


    def shoot_ultra_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots ultra bullets.
        """

        center_x, center_y = self.center

        bullets.append(BulletAccel(cx=center_x,
                                   cy=center_y - self.bul_aux_y,
                                   radius=self.bul_rad_aux,
                                   health=1,
                                   how_hard=self.hardness,
                                   speed=4.0))

        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=3,
                                              how_hard=self.hardness,
                                              speed=5.5,
                                              first_to_right=False))
        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=2,
                                              how_hard=self.hardness,
                                              speed=5.5,
                                              amplitude=18.0,
                                              first_to_right=False))
        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=3,
                                              how_hard=self.hardness,
                                              speed=4.5,
                                              first_to_right=False))
        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=3,
                                              how_hard=self.hardness,
                                              speed=4.4,
                                              first_to_right=True))
        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=2,
                                              how_hard=self.hardness,
                                              speed=5.5,
                                              amplitude=18.0,
                                              first_to_right=True))
        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=3,
                                              how_hard=self.hardness,
                                              speed=5.4,
                                              first_to_right=True))


    def shoot_mega_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots mega bullets.
        """

        center_x, center_y = self.center

        bullets.append(BulletElectric(cx=center_x,
                                      cy=center_y - self.bul_aux_y,
                                      radius=self.bul_rad_aux,
                                      health=4,
                                      how_hard=self.hardness,
                                      speed=5.0,

                                      # Electric
                                      radar_pool=self.threats_pool))


    def shoot_hyper_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots hyper bullets.
        """

        center_x, center_y = self.center
        field_rad = WIDTH / 30

        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=5,
                                    how_hard=self.hardness,
                                    speed=5.5,
                                    sprite_type=BulletSprites.SPECIAL,
                                    angle=radians(86.0)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=5,
                                    how_hard=self.hardness,
                                    speed=5.0,
                                    sprite_type=BulletSprites.SPECIAL,
                                    angle=radians(88.0)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=5,
                                    how_hard=self.hardness,
                                    speed=5.5,
                                    sprite_type=BulletSprites.SPECIAL,
                                    angle=radians(90.0)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=5,
                                    how_hard=self.hardness,
                                    speed=5.0,
                                    sprite_type=BulletSprites.SPECIAL,
                                    angle=radians(92.0)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=5,
                                    how_hard=self.hardness,
                                    speed=5.5,
                                    sprite_type=BulletSprites.SPECIAL,
                                    angle=radians(94.0)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=5,
                                    how_hard=self.hardness,
                                    speed=4.5,
                                    sprite_type=BulletSprites.SPECIAL,
                                    angle=radians(90.0)))

        bullets.append(BulletElectric(cx=center_x,
                                      cy=center_y - self.bul_aux_y,
                                      radius=self.bul_rad_aux,
                                      health=5,
                                      how_hard=self.hardness,
                                      speed=4.0,
                                      ethereal=True,

                                      # Electric
                                      angle=radians(75.0),
                                      radar_pool=self.threats_pool,
                                      field_radius=field_rad))
        bullets.append(BulletElectric(cx=center_x,
                                      cy=center_y - self.bul_aux_y,
                                      radius=self.bul_rad_aux,
                                      health=5,
                                      how_hard=self.hardness,
                                      speed=4.0,
                                      ethereal=True,

                                      # Electric
                                      angle=radians(90.0),
                                      radar_pool=self.threats_pool,
                                      field_radius=field_rad))
        bullets.append(BulletElectric(cx=center_x,
                                      cy=center_y - self.bul_aux_y,
                                      radius=self.bul_rad_aux,
                                      health=5,
                                      how_hard=self.hardness,
                                      speed=4.0,
                                      ethereal=True,

                                      # Electric
                                      angle=radians(105.0),
                                      radar_pool=self.threats_pool,
                                      field_radius=field_rad))
