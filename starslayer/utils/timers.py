"""
Timers Module. Contains simple timers to
handle event timing.
"""

class Timer:
    """
    Class for a simple timer that counts
    from a certain number to 0.
    """

    def __init__(self, init_time: int, message: str='') -> None:
        """
        Initializes an instance of type 'Timer'.
        """

        self.initial_time = init_time
        self.current_time = init_time
        self.msg = message


    def __str__(self) -> str:
        """
        Returns a string with class information so it can be printed later.
        """

        return (f"Initial Time: {self.initial_time} - Current Time: {self.current_time}" +
                f"{f' - Message: {self.msg}' if self.msg != '' else ''}")


    def deduct(self, how_much: int) -> None:
        """
        Descends the countdown subtracting 'how_much' time from 'self.current_time'.
        """

        self.current_time -= how_much


    def count(self, how_much: int, reset: bool=False) -> None:
        """
        Count the timer to zero.
        if 'reset' is set to 'True', it automatically restarts the timer.
        """

        if not self.is_zero_or_less():

            self.deduct(how_much)

        elif reset:

            self.reset()


    def reset(self) -> None:
        """
        Resets the timer to its original value ('self.initial_value').
        """

        self.current_time = self.initial_time
        self.msg = ''


    def is_zero_or_less(self) -> bool:
        """
        Returns 'True' if the current time of the Timer reaches zero (0) or further,
        and 'False' otherwise.
        """

        return self.current_time <= 0


    def change_message(self, new_message: str) -> None:
        """
        Changes the current message to a given new one.
        """

        self.msg = new_message


class SpringTimer:
    """
    Simple timer that oscillates between
    given 'floor' and 'ceiling' values.
    """

    def __init__(self,
                 floor: int,
                 ceiling: int,
                 where_to_start: int,
                 is_it_adding: bool=True) -> None:
        """
        Initializes an instance of type 'SpringTimer'.
        """

        if floor >= ceiling:

            raise ValueError("'floor' parameter must NOT be greater or equal than 'ceiling'")

        if where_to_start < floor or where_to_start > ceiling:

            raise ValueError("'where_to_start' parameter needs to be between " +
                             f"{floor} and {ceiling} inclusive")

        self.floor = floor
        self.ceil = ceiling
        self.current = where_to_start
        self.adding = is_it_adding


    def __str__(self) -> str:
        """
        Returns a string with class information so it can be printed later.
        """

        return (f"Current: {self.current} - Floor: {self.floor} - " +
                f"Ceiling: {self.ceil} - Is it adding: {self.adding}")


    def count(self, how_much: int=1) -> None:
        """
        Advances the counting of the Timer, deducting if 'self.adding' is False, otherwise adding.
        """

        if self.adding:

            if self.current < self.ceil:

                self.current += how_much
        else:

            if self.current > self.floor:

                self.current -= how_much

        if any((self.current <= self.floor, self.current >= self.ceil)):

            self.adding = not self.adding
