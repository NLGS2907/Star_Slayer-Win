"""
Bilby Tanka character Module.
"""

from math import pi as PI
from math import radians
from typing import TYPE_CHECKING, List, Optional

from ..bullets import (BulletInvisible, BulletOrbiting, BulletRadial,
                       BulletSpiralAlt, BulletSprites)
from ..consts import BILBY_TANKA_REL_PATH, HEIGHT, WIDTH
from .playable_character import PlayableCharacter
from .satellites import Cannon

if TYPE_CHECKING:
    from ..bullets import Bullet
    from ..state import Game


class BilbyTankaCharacter(PlayableCharacter):
    """
    The Bilby Tanka playable character.

    Its special power resides in a very powerful bullet field,
    used as shield.
    """

    # pylint: disable=invalid-name
    def __init__(self, **kwargs) -> None:
        """
        Initializes an instance of type 'BilbyTankaCharacter'.
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
                         health=200,
                         how_hard=5,
                         speed=3,
                         texture_path=BILBY_TANKA_REL_PATH,
                         has_satellite=True,
                         satellite_type=Cannon,
                         sat_x=x2 + width_aux,
                         sat_y=y1 - height_aux,
                         sat_rad=width_aux * 0.8,
                         **kwargs)

        self._to_right: bool = True


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

        how_many = 12
        augment  = (2 * PI) / how_many
        center_x, center_y = self.center
        self.bul_rad_aux = WIDTH // 150

        for i in range(how_many):
            game.player_bullets.append(BulletOrbiting(cx=center_x,
                                                      cy=center_y,
                                                      radius=self.bul_rad_aux,
                                                      health=2,
                                                      speed=0.8,
                                                      how_hard=game.player.hardness,
                                                      starting_angle=(i * augment),
                                                      orbit_center=game.player,
                                                      time_until_orbit=30.0))
            game.player_bullets.append(BulletOrbiting(cx=center_x,
                                                      cy=center_y,
                                                      radius=self.bul_rad_aux,
                                                      health=2,
                                                      speed=0.9,
                                                      how_hard=game.player.hardness,
                                                      starting_angle=(i * 1.2 * augment),
                                                      orbit_center=game.player,
                                                      time_until_orbit=25.0,
                                                      clockwise=True))
            game.player_bullets.append(BulletOrbiting(cx=center_x,
                                                      cy=center_y,
                                                      radius=self.bul_rad_aux,
                                                      health=2,
                                                      speed=1.0,
                                                      how_hard=game.player.hardness,
                                                      starting_angle=(i * 1.5 * augment),
                                                      orbit_center=game.player,
                                                      time_until_orbit=20.0))

        self.reset_ability_points()


    def _change_direction(self) -> None:
        """
        Alternates between shooting the bullet left or right.
        """

        self._to_right = not self._to_right


    def _cannon_angle(self) -> float:
        """
        Returns the angle towards the satellite (most
        likely a cannon).
        """

        if self.satellite is None:
            return radians(90.0)

        return self.angle_towards(self.satellite)


    def _shoot_bullet_ring(self,
                           bullets: List["Bullet"],
                           anchor_bullet: "Bullet",
                           *,
                           sprite_type: Optional[BulletSprites]=None,
                           how_many_satellites: int=8,
                           initial_phase: float=90.0,
                           initial_radius: float=40.0,
                           orbit_health: int=1,
                           orbit_speed: float=0.5) -> None:
        """
        Shoots a ring of bullets.
        """

        center_x, center_y = anchor_bullet.center
        augment = 360 / how_many_satellites

        anchor_bullet.is_ethereal = True # The anchor cannot die

        for i in range(how_many_satellites):
            bullets.append(BulletOrbiting(cx=center_x,
                                          cy=center_y,
                                          radius=self.bul_rad_aux,
                                          health=orbit_health,
                                          speed=orbit_speed,
                                          how_hard=self.hardness,
                                          sprite_type=sprite_type,

                                          # Orbiting
                                          starting_angle=radians((i * augment) + initial_phase),
                                          initial_radius=initial_radius,
                                          orbit_center=anchor_bullet,
                                          time_until_orbit=0.0,
                                          curvature_speed=0.07))



    def shoot_simple_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots simple bullets.
        """

        center_x, center_y = self.center

        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y,
                                    radius=self.bul_rad_aux,
                                    health=1,
                                    speed=5,
                                    how_hard=self.hardness,

                                    # rad
                                    angle=self._cannon_angle()))

        bullets.append(BulletSpiralAlt(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=2,
                                       how_hard=int(self.hardness * 1.5),
                                       speed=5,
                                       first_to_right=self._to_right))

        self._change_direction()


    def shoot_super_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots super bullets.
        """

        center_x, center_y = self.center

        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y,
                                    radius=self.bul_rad_aux,
                                    health=2,
                                    speed=5,
                                    how_hard=self.hardness,

                                    # rad
                                    angle=self._cannon_angle()))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y,
                                    radius=self.bul_rad_aux,
                                    health=2,
                                    speed=4,
                                    how_hard=self.hardness,

                                    # rad
                                    angle=self._cannon_angle()))

        bullets.append(BulletSpiralAlt(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=3,
                                       how_hard=int(self.hardness * 1.5),
                                       speed=5,
                                       first_to_right=False))
        bullets.append(BulletSpiralAlt(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=3,
                                       how_hard=int(self.hardness * 1.5),
                                       speed=5,
                                       first_to_right=True))


    def shoot_ultra_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots ultra bullets.
        """

        center_x, center_y = self.center

        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y,
                                    radius=self.bul_rad_aux,
                                    health=2,
                                    speed=6,
                                    how_hard=self.hardness,

                                    # rad
                                    angle=self._cannon_angle() - radians(5)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y,
                                    radius=self.bul_rad_aux,
                                    health=2,
                                    speed=5.5,
                                    how_hard=self.hardness,

                                    # rad
                                    angle=self._cannon_angle() - radians(2.5)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y,
                                    radius=self.bul_rad_aux,
                                    health=2,
                                    speed=6,
                                    how_hard=self.hardness,

                                    # rad
                                    angle=self._cannon_angle()))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y,
                                    radius=self.bul_rad_aux,
                                    health=2,
                                    speed=5.5,
                                    how_hard=self.hardness,

                                    # rad
                                    angle=self._cannon_angle() + radians(2.5)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y,
                                    radius=self.bul_rad_aux,
                                    health=2,
                                    speed=6,
                                    how_hard=self.hardness,

                                    # rad
                                    angle=self._cannon_angle() + radians(5)))

        bullets.append(BulletSpiralAlt(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=3,
                                       how_hard=int(self.hardness * 1.5),
                                       speed=5,
                                       starting_angle=self._cannon_angle(),
                                       first_to_right=False))
        bullets.append(BulletSpiralAlt(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=3,
                                       how_hard=int(self.hardness * 1.5),
                                       speed=5,
                                       starting_angle=self._cannon_angle(),
                                       first_to_right=True))


    def shoot_mega_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots mega bullets.
        """

        center_x, center_y = self.center

        anchor = BulletInvisible(cx=center_x,
                                 cy=center_y - self.bul_aux_y,
                                 radius=self.bul_rad_aux,
                                 speed=8,
                                 angle=self._cannon_angle())

        bullets.append(anchor)
        self._shoot_bullet_ring(bullets, anchor)


    def shoot_hyper_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots hyper bullets.
        """

        center_x, center_y = self.center

        first_anchor = BulletInvisible(cx=center_x,
                                 cy=center_y - self.bul_aux_y,
                                 radius=self.bul_rad_aux,
                                 speed=8,
                                 angle=self._cannon_angle())

        second_anchor = BulletSpiralAlt(cx=center_x,
                                        cy=center_y - self.bul_aux_y,
                                        radius=self.bul_rad_aux,
                                        health=3,
                                        how_hard=int(self.hardness * 1.5),
                                        speed=7.6,
                                        sprite_type=BulletSprites.SPECIAL,

                                        # Spiral
                                        starting_angle=self._cannon_angle(),
                                        first_to_right=False)
        third_anchor = BulletSpiralAlt(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=3,
                                       how_hard=int(self.hardness * 1.5),
                                       speed=8,
                                       sprite_type=BulletSprites.SPECIAL,

                                       # Spiral
                                       starting_angle=self._cannon_angle(),
                                       first_to_right=True)

        bullets.append(first_anchor)
        self._shoot_bullet_ring(bullets, first_anchor,
                                how_many_satellites=4,
                                initial_radius=25.0,
                                sprite_type=BulletSprites.SPECIAL)

        bullets.append(second_anchor)
        self._shoot_bullet_ring(bullets, second_anchor,
                                how_many_satellites=3,
                                initial_radius=35.0,
                                sprite_type=BulletSprites.SPECIAL)

        bullets.append(third_anchor)
        self._shoot_bullet_ring(bullets, third_anchor,
                                how_many_satellites=3,
                                initial_radius=35.0,
                                sprite_type=BulletSprites.SPECIAL)
