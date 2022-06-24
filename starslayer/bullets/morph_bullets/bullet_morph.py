"""
A bullet that transforms into another.
"""

from typing import List

from ...utils import Timer
from ..bullet import Bullet, BulletKwargs


class BulletMorph(Bullet):
    """
    A bullet that changes its form of trajectory,
    imitating other bullets.
    """

    def __init__(self,
                 *,
                 shapes: List[Bullet],
                 morphing_time: float=100.0,
                 morph_chances: int=-1,
                 loops: int=0,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletMorph'.

        It must provide all the parameters for all the shapes declared.
        """

        super().__init__(**kwargs)

        if not shapes:
            ValueError("shapes list must contain at least 1 value.")

        self.morphing: Timer = Timer(morphing_time)
        self.chances: int = ((len(shapes) * loops) - 1 if loops > 0 else morph_chances)
        self.times_morphed: int = 0
        self.forms: List[Bullet] = [shape(**kwargs) for shape in shapes]
        self.current_form: Bullet = self.forms[0]


    def can_transform(self) -> bool:
        """
        Checks if the bullet can transform into another.
        """

        return self.chances > 0 and self.times_morphed < self.chances


    def next_form(self) -> None:
        """
        Changes into the next form.
        """

        ind = self.forms.index(self.current_form)
        self.current_form = self.forms[(ind + 1) % len(self.forms)]


    def trajectory(self) -> None:
        """
        Defines the trajectory of a morphing bullet.
        """

        self.current_form.trajectory()
        self.cx, self.cy = self.current_form.center

        self.morphing.count(1.0, reset=True)

        if self.morphing.time_is_up() and self.can_transform():
            self.next_form()
            self.current_form.cx, self.current_form.cy = self.center
            self.times_morphed += 1
