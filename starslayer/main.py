"""
Main Module. It encases all the other modules to start the game.
"""

from .consts import GAME_ICON, GAME_VERSION, HEIGHT, WIDTH
from .gamelib import (draw_begin, draw_end, get_events, icon, init, loop,
                      resize, title)
from .graphics import SceneDrawer, draw_screen
from .state import Game


def main() -> int:
    """
    Main function. Initializes the game.
    """

    title(f"Star Slayer v{GAME_VERSION}")
    resize(WIDTH, HEIGHT)
    icon(GAME_ICON)

    game = Game()
    scene_drawer = SceneDrawer(game)

    is_first_lap = True # So that some actions take place in the next iteration of the loop
    cursor_coords = {'x': None, 'y': None}

    while loop(fps=game.time_flow):

        if game.exit:
            break

        draw_begin()
        cursor_x, cursor_y = cursor_coords['x'], cursor_coords['y']
        draw_screen(game, cursor_x, cursor_y, scene_drawer)
        draw_end()

        for event in get_events():

            if not event:
                break

            game.classify_events(event, cursor_coords)

        game.process_events()

        if game.is_on_prompt:

            if is_first_lap:
                is_first_lap = False

            else:
                is_first_lap = True
                game.prompt()

        # print(game.typing_cooldown.current_time)
        # print(game.combinations)
        game.advance_game()

    return 0


if __name__ == "__main__":

    init(main)
