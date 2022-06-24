"""
Cheats group for twisting the rules.
"""

from typing import TYPE_CHECKING

from ...checks import is_in_game
from ...consts import HEIGHT, SFX_CHEAT_USED, WIDTH
from ...drops import MedKit, RadialBomb, SpiralBomb
from ..hooks_group import HooksGroup

if TYPE_CHECKING:
    from ...state import Game


class Cheats(HooksGroup):
    """
    Cheats Group.
    """

    @HooksGroup.combination(with_name="points")
    @is_in_game()
    def add_five_hundred_points(self) -> None:
        """
        Adds 500 points to the game score.
        """

        self.game.score += 500


    @HooksGroup.combination(with_name="gimmepoints")
    @is_in_game()
    def add_one_thousand_points(self) -> None:
        """
        Adds 1000 points to the game score.
        """

        self.game.score += 1000


    @HooksGroup.combination(with_name="gimmemorepoints")
    @is_in_game()
    def add_five_thousand_points(self) -> None:
        """
        Adds 5000 points to the game score.
        """

        self.game.score += 5000


    @HooksGroup.combination(with_name="immabitchforpoints")
    @is_in_game()
    def add_ten_thousand_points(self) -> None:
        """
        Adds 10000 points to the game score.
        """

        self.game.score += 10000


    @HooksGroup.combination(with_name="POINTS")
    @is_in_game()
    def add_twenty_thousand_points(self) -> None:
        """
        Adds 20000 points to the game score.
        """

        self.game.score += 20000


    @HooksGroup.combination(with_name="gimmeability")
    @is_in_game()
    def give_little_ability_points(self) -> None:
        """
        Adds a few points to the ability gauge for utilizing
        the player's ability.
        """

        self.game.player.add_ability_points(200)


    @HooksGroup.combination(with_name="fullability")
    @is_in_game()
    def fill_ability_gauge(self) -> None:
        """
        Adds enough points to the ability gauge for utilizing
        the player's ability.
        """

        self.game.player.add_ability_points(self.game.player.ability_threshold)


    @HooksGroup.combination(with_name="imfastasfboi")
    @is_in_game()
    def great_velocity(self) -> None:
        """
        Greatly augments player's velocity.
        """

        self.game.player.speed += 50


    @HooksGroup.combination(with_name="ghosted")
    @is_in_game()
    def be_ethereal(self) -> None:
        """
        Nullifies the player's hitbox.
        """

        self.game.player.is_ethereal = True


    @HooksGroup.combination(with_name="unghost")
    @is_in_game()
    def unbe_ethereal(self) -> None:
        """
        Reconstructs the player's hitbox.
        """

        self.game.player.is_ethereal = False


    @HooksGroup.combination(with_name="allshallperish")
    @is_in_game()
    def bullet_minigun(self) -> None:
        """
        Turns off the shooting cooldown.
        """

        self.game.player.change_cooldown(2)


    @HooksGroup.combination(with_name="allshallbeforgiven")
    @is_in_game()
    def bullet_back_to_normal(self) -> None:
        """
        Turns back on the shooting cooldown.
        """

        self.game.player.change_cooldown(self.game.player.power_level.cooldown)


    @HooksGroup.combination(with_name="imdie")
    @is_in_game()
    def thank_you_forever(self) -> None:
        """
        Insta-kills the player.
        """

        self.game.player.die()


    @HooksGroup.combination(with_name="medkit")
    @is_in_game()
    def grant_health(self) -> None:
        """
        Spawns a medkit drop.
        """

        pl_x, pl_y = self.game.player.center
        height_aux = HEIGHT / 7
        width = WIDTH / 25
        height = HEIGHT / 23

        self.game.drops.append(MedKit(x1=pl_x - (width / 2),
                                      y1=pl_y - height_aux - (height / 2),
                                      x2=pl_x + (width / 2),
                                      y2=pl_y - height_aux + (height / 2)))


    @HooksGroup.combination(with_name="dropbomb")
    @is_in_game()
    def drop_bomb(self) -> None:
        """
        Drops a bomb of radial bullets.
        """

        pl_x, pl_y = self.game.player.center
        height_aux = HEIGHT / 7
        width = WIDTH / 25
        height = HEIGHT / 23

        self.game.drops.append(RadialBomb(x1=pl_x - (width / 2),
                                          y1=pl_y - height_aux - (height / 2),
                                          x2=pl_x + (width / 2),
                                          y2=pl_y - height_aux + (height / 2)))


    @HooksGroup.combination(with_name="spiralbomb")
    @is_in_game()
    def drop_spiral_bomb(self) -> None:
        """
        Drops a bomb of spiral bullets.
        """

        pl_x, pl_y = self.game.player.center
        height_aux = HEIGHT / 7
        width = WIDTH / 25
        height = HEIGHT / 23

        self.game.drops.append(SpiralBomb(x1=pl_x - (width / 2),
                                          y1=pl_y - height_aux - (height / 2),
                                          x2=pl_x + (width / 2),
                                          y2=pl_y - height_aux + (height / 2)))


    def post_hook(self) -> None:
        """
        Makes a sound indicating that the cheat was executed.
        """

        self.game.used_cheats = True
        self.game.play_sound(SFX_CHEAT_USED)


def setup_hook(game: "Game") -> None:
    """
    Adds the hook group in this file to the game.
    """

    game.add_group(Cheats(game))
