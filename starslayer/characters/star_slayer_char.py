"""
Star Slayer character Module.
"""

from math import radians
from typing import TYPE_CHECKING, List

from ..bullets import (BulletHoming, BulletMorph, BulletAccel,
                       BulletRadial, BulletSinusoidalSimple,
                       BulletSpiralSimple, BulletSprites, BulletFirework)
from ..consts import HEIGHT, STAR_SLAYER_REL_PATH, WIDTH
from ..utils import Timer
from .playable_character import PlayableCharacter

if TYPE_CHECKING:
    from ..bullets import Bullet
    from ..state import Game
    from ..utils import BoundingShape


class StarSlayerCharacter(PlayableCharacter):
    """
    The star slayer playable character.

    Its special power resides in homing bullets.
    """

    # pylint: disable=invalid-name
    def __init__(self, **kwargs) -> None:
        """
        Initializes an instance of type 'StarSlayerCharacter'.
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
                         health=100,
                         how_hard=2,
                         speed=5,
                         texture_path=STAR_SLAYER_REL_PATH,
                         **kwargs)

        self.ability_timer: Timer = Timer(1000.0)
        self.ability_timer.drop()
        self.homing_targets: List["BoundingShape"] = []


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

        self.homing_targets = game.enemies
        self.ability_timer.reset()
        self.reset_ability_points()


    def _is_using_ability(self) -> bool:
        """
        Wrapper for checking if the player activated the ability.
        """

        return not self.ability_timer.time_is_up()


    def _can_shoot_homing(self) -> bool:
        """
        Checks if the target pool isn't empty.
        """

        return self._is_using_ability() and self.homing_targets


    def refresh_hook(self) -> None:
        """
        Updates the ability timer.
        """

        percentage = (self.ability_timer.current_time / self.ability_timer.base_time) * 100

        self.ability_timer.count(1.0)

        if self._is_using_ability():
            self.change_ability_gauge_percentage(percentage)


    def _shoot_radial_homing(self,
                             bullets: List["Bullet"],
                             *,
                             how_many: int=1,
                             initial_phase: float=90.0,
                             health: int=1,
                             speed: float=5.0) -> None:
        """
        Shoots a certain amount of morphing bullets, transforming
        from radial bullets to homing ones.
        """

        center_x, center_y = self.center
        augment = 360 / how_many

        for i in range(how_many):
            bullets.append(BulletMorph(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=health,
                                       how_hard=self.hardness,
                                       speed=speed,
                                       sprite_type=BulletSprites.SHINY,

                                       # Morph
                                       shapes=[BulletRadial, BulletHoming],
                                       morphing_time=25.0,
                                       morph_chances=1,

                                       # Rad
                                       angle=radians(i * augment + initial_phase),

                                       # Homing
                                       homing_time=100.0,
                                       target_pool=self.homing_targets))


    def shoot_simple_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots simple bullets.
        """

        center_x, center_y = self.center

        if self._can_shoot_homing():
            bullets.append(BulletHoming(cx=center_x,
                                        cy=center_y - self.bul_aux_y,
                                        radius=self.bul_rad_aux,
                                        health=1,
                                        how_hard=self.hardness,
                                        speed=5,
                                        homing_time=100.0,
                                        target_pool=self.homing_targets,
                                        sprite_type=BulletSprites.SHINY))
            return

        bullets.append(BulletAccel(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=1,
                                       how_hard=self.hardness,
                                       speed=5))


    def shoot_super_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots super bullets.
        """

        center_x, center_y = self.center

        if self._can_shoot_homing():
            self._shoot_radial_homing(bullets,
                                      how_many=3)
            return

        bullets.append(BulletAccel(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=2,
                                       how_hard=self.hardness,
                                       speed=5))
        bullets.append(BulletRadial(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=2,
                                       how_hard=self.hardness,
                                       speed=5,
                                       angle=radians(75.0)))
        bullets.append(BulletRadial(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=2,
                                       how_hard=self.hardness,
                                       speed=5,
                                       angle=radians(105.0)))


    def shoot_ultra_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots ultra bullets.
        """

        center_x, center_y = self.center

        if self._can_shoot_homing():
            self._shoot_radial_homing(bullets,
                                      how_many=5)
            return

        bullets.append(BulletAccel(cx=center_x,
                                   cy=center_y - self.bul_aux_y,
                                   radius=self.bul_rad_aux,
                                   health=3,
                                   how_hard=self.hardness,
                                   speed=5))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=3,
                                    how_hard=self.hardness,
                                    speed=4,
                                    angle=radians(75.0)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=3,
                                    how_hard=self.hardness,
                                    speed=5,
                                    angle=radians(65.0)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=3,
                                    how_hard=self.hardness,
                                    speed=4,
                                    angle=radians(105.0)))
        bullets.append(BulletRadial(cx=center_x,
                                    cy=center_y - self.bul_aux_y,
                                    radius=self.bul_rad_aux,
                                    health=3,
                                    how_hard=self.hardness,
                                    speed=5,
                                    angle=radians(115.0)))


    def shoot_mega_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots mega bullets.
        """

        center_x, center_y = self.center

        if self._can_shoot_homing():
            self._shoot_radial_homing(bullets,
                                      how_many=7)
            return

        bullets.append(BulletRadial(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=2,
                                       how_hard=self.hardness,
                                       speed=5,
                                       angle=radians(85.0)))
        bullets.append(BulletRadial(cx=center_x,
                                       cy=center_y - self.bul_aux_y,
                                       radius=self.bul_rad_aux,
                                       health=2,
                                       how_hard=self.hardness,
                                       speed=5,
                                       angle=radians(95.0)))

        bullets.append(BulletSpiralSimple(cx=center_x,
                                          cy=center_y - self.bul_aux_y,
                                          radius=self.bul_rad_aux,
                                          health=4,
                                          how_hard=self.hardness * 1.1,
                                          speed=1,

                                          #Spiral
                                          clockwise=False,
                                          starting_angle=radians(0.0),
                                          radius_speed=0.4))

        bullets.append(BulletSpiralSimple(cx=center_x,
                                          cy=center_y - self.bul_aux_y,
                                          radius=self.bul_rad_aux,
                                          health=4,
                                          how_hard=self.hardness * 1.1,
                                          speed=1,

                                          #Spiral
                                          clockwise=True,
                                          starting_angle=radians(180.0),
                                          radius_speed=0.4))

        bullets.append(BulletSpiralSimple(cx=center_x,
                                          cy=center_y - self.bul_aux_y,
                                          radius=self.bul_rad_aux,
                                          health=4,
                                          how_hard=self.hardness * 1.1,
                                          speed=0.9,

                                          # Spiral
                                          clockwise=False,
                                          starting_angle=radians(10.0),
                                          radius_speed=0.3))

        bullets.append(BulletSpiralSimple(cx=center_x,
                                          cy=center_y - self.bul_aux_y,
                                          radius=self.bul_rad_aux,
                                          health=4,
                                          how_hard=self.hardness * 1.1,
                                          speed=0.9,

                                          # Spiral
                                          clockwise=True,
                                          starting_angle=radians(190.0),
                                          radius_speed=0.3))

        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=4,
                                              how_hard=self.hardness * 1.1,
                                              speed=4.3,

                                              # Sinusoidal
                                              amplitude=17.0,
                                              first_to_right=True))

        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=4,
                                              how_hard=self.hardness * 1.1,
                                              speed=5,

                                              # Sinusoidal
                                              amplitude=17.0,
                                              first_to_right=True))

        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=4,
                                              how_hard=self.hardness * 1.1,
                                              speed=4.3,

                                              # Sinusoidal
                                              amplitude=17.0,
                                              first_to_right=False))

        bullets.append(BulletSinusoidalSimple(cx=center_x,
                                              cy=center_y - self.bul_aux_y,
                                              radius=self.bul_rad_aux,
                                              health=4,
                                              how_hard=self.hardness * 1.1,
                                              speed=5,

                                              # Sinusoidal
                                              amplitude=17.0,
                                              first_to_right=False))


    def shoot_hyper_bullets(self, bullets: List["Bullet"]) -> None:
        """
        Shoots hyper bullets.
        """

        center_x, center_y = self.center

        if self._can_shoot_homing():
            self._shoot_radial_homing(bullets,
                                      how_many=5,
                                      health=2,
                                      speed=6.5)
            self._shoot_radial_homing(bullets,
                                      how_many=5,
                                      health=2,
                                      initial_phase=45.0,
                                      speed=4.2)
            return

        bullets.append(BulletFirework(cx=center_x,
                                      cy=center_y - self.bul_aux_y,
                                      radius=self.bul_rad_aux,
                                      health=5,
                                      how_hard=self.hardness * 1.2,
                                      speed=6,
                                      sprite_type=BulletSprites.SPECIAL,

                                      # Fireworks
                                      angle=radians(90.0),
                                      bullets_pool=bullets,
                                      how_many_children=6))
        bullets.append(BulletFirework(cx=center_x,
                                      cy=center_y - self.bul_aux_y,
                                      radius=self.bul_rad_aux,
                                      health=5,
                                      how_hard=self.hardness * 1.2,
                                      speed=6,
                                      sprite_type=BulletSprites.SPECIAL,

                                      # Fireworks
                                      angle=radians(60.0),
                                      bullets_pool=bullets))

        bullets.append(BulletFirework(cx=center_x,
                                      cy=center_y - self.bul_aux_y,
                                      radius=self.bul_rad_aux,
                                      health=5,
                                      how_hard=self.hardness * 1.2,
                                      speed=6,
                                      sprite_type=BulletSprites.SPECIAL,

                                      # Fireworks
                                      angle=radians(120.0),
                                      bullets_pool=bullets))
