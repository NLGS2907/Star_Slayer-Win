"""
Main Module. It encases all the other modules to start the game.
"""

from .consts import GAME_VERSION, HEIGHT, KEYS_PATH, PLAYER_SPRITE, WIDTH
from .files import list_repeated_keys, load_json
from .gamelib import (EventType, draw_begin, draw_end, get_events, icon, init,
                      loop, resize, title)
from .graphics import draw_screen
from .state import Game


def main() -> int:
    """
    Main function. Initializes the game.
    """

    title(f"Star Slayer v{GAME_VERSION}")
    resize(WIDTH, HEIGHT)
    icon(PLAYER_SPRITE)

    game = Game(initial_power=3)

    keys_pressed = {}
    events_processed = {}

    is_first_lap = True # So that some actions take place in the next iteration of the loop

    while loop(fps=60):

        if game.exit:
            break

        draw_begin()
        draw_screen(game)
        draw_end()

        for event in get_events():

            if not event:
                break

            if event.type == EventType.KeyPress:

                keys_pressed[event.key] = True

            elif event.type == EventType.KeyRelease:

                keys_pressed[event.key] = False

            elif event.type == EventType.ButtonPress:

                if event.mouse_button == 1:

                    game.execute_button(event.x, event.y)

        for key in keys_pressed:

            action = game.process_key(key)

            if keys_pressed.get(key, False):

                events_processed[action] = True

            elif all((not keys_pressed.get(repeated_key, False)
                      for repeated_key in list_repeated_keys(action, load_json(KEYS_PATH)))):

                events_processed[action] = False

        for game_action in events_processed:

            if events_processed.get(game_action, False):

                game.execute_action(game_action)

        if game.is_on_prompt:

            if is_first_lap:

                is_first_lap = False

            else:

                is_first_lap = True
                game.prompt()

        game.advance_game(keys_pressed)

    return 0


if __name__ == "__main__":

    init(main)
