import gamelib, graphics, game_state, files

def main():

    gamelib.title(f"Star Slayer (Pre)")
    gamelib.resize(files.EXT_CONST["WIDTH"], files.EXT_CONST["HEIGHT"])

    game = game_state.Game(inital_power=1)

    keys_pressed = dict()

    while gamelib.loop(fps=60):

        if game.exit:
            break

        gamelib.draw_begin()
        graphics.draw_screen(game)
        gamelib.draw_end()

        for event in gamelib.get_events():

            if not event:  
                break

            if event.type == gamelib.EventType.KeyPress:

                keys_pressed[event.key] = True

            if event.type == gamelib.EventType.KeyRelease:

                keys_pressed[event.key] = False

            if event.type == gamelib.EventType.ButtonPress:

                if event.mouse_button == 1:

                    game.process_click(event.x, event.y)

        for key in keys_pressed:

            if keys_pressed.get(key, False): game.process_action(game.process_key(key))

        game.advance_game()

if __name__ == "__main__":

    gamelib.init(main)