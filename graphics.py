import gamelib, files

WIDTH, HEIGHT = files.EXT_CONST['WIDTH'], files.EXT_CONST['HEIGHT']
GUI_SPACE = files.EXT_CONST['GUI_SPACE']
DEBUG_LINES = files.EXT_CONST['DEBUG_LINES'] # Additional information on DEBUG action.

def draw_background():
    """
    ______________________________________________________________________

    ---> None
    ______________________________________________________________________

    Draws the background of the game (duh).
    """
    gamelib.draw_rectangle(0, 0, WIDTH, HEIGHT, fill='#00102b')

def draw_GUI(game):
    """
    ______________________________________________________________________

    game: <Game>


    ---> None
    ______________________________________________________________________

    Draws the User Interface.
    """
    gamelib.draw_rectangle(WIDTH - GUI_SPACE, 0, WIDTH, HEIGHT, outline='', fill='#333333')

    gamelib.draw_text(f"Time: {game.level_timer.current_time}", (WIDTH - GUI_SPACE) + 10, 10, anchor='nw')

def draw_menus(game):
    """
    ______________________________________________________________________

    game: <Game>


    ---> None
    ______________________________________________________________________

    Draws in the screen the current selected menu.
    """
    menu = game.menu_in_display

    if menu == game.main_menu:

        gamelib.draw_text("STAR\nSLAYER", WIDTH // 2, HEIGHT // 4, size=(WIDTH // 10), justify='c')

    elif menu == game.options_menu:

        gamelib.draw_text("OPTIONS", WIDTH // 2, HEIGHT // 4, size=(WIDTH // 10), justify='c')

    elif menu == game.controls_menu:

        draw_changeable_buttons(game)

    draw_menu_buttons(menu)


def draw_changeable_buttons(game):
    """
    ______________________________________________________________________

    game: <Game>


    ---> None
    ______________________________________________________________________

    Draws the information of the action and its assigned keys.
    If possible, it also allows it to edit said information.
    """
    aux = (HEIGHT // 70)

    gamelib.draw_text("CONTROLS", (WIDTH // 8) + 5, (HEIGHT // 15), size=(HEIGHT // 32), justify='c')
    gamelib.draw_rectangle((WIDTH // 4) + aux, aux, WIDTH - aux, HEIGHT - aux, width=(HEIGHT // 87), outline="#001d4d", fill="#00173d")
    gamelib.draw_text(f"{game.action_to_show}", (WIDTH * (5 / 8)), (HEIGHT // 8), fill="#ffffff", size=72, justify='c')

    keys_assigned = files.list_repeated_keys(game.action_to_show, files.map_keys())

    gamelib.draw_text(','.join(keys_assigned),
                        (WIDTH * (5 / 8)), (HEIGHT / 2.5), fill="#ffffff", size=30, justify='c')

    gamelib.draw_text(f"Action is currently bound to the key{'s' if len(keys_assigned) > 1 else ''}", (WIDTH * (5 / 8)), (HEIGHT / 3.5), fill="#ffffff", size=22, justify='c')

    draw_menu_buttons(game.sub_menu)

def draw_menu_buttons(menu):
    """
    ______________________________________________________________________

    menu: <Menu>


    ---> None
    ______________________________________________________________________

    Draws all the buttons of a given menu.
    """
    for button in menu.buttons_on_screen:

        gamelib.draw_rectangle(button.x1, button.y1, button.x2, button.y2, width=2, outline='#ffffff', fill='#474747', activefill='#7a7a7a')
    
        if button.msg:

            center_x, center_y = button.center()
            gamelib.draw_text(button.msg, center_x, center_y, size=(HEIGHT // 43), fill='#ffffff', justify='c')

def draw_ship(ship, which_one=0):
    """
    ______________________________________________________________________

    ship: <Ship>

    which_one: <int>


    ---> None
    ______________________________________________________________________

    Draws the sprite of a ship.

    'which_one' refers to which frame to draw.
    """
    if ship.sprites == None:

        gamelib.draw_rectangle(ship.x1, ship.y1, ship.x2, ship.y2, fill='red')

    else:

        gamelib.draw_image(ship.sprites[which_one], ship.x1, ship.y1)

def draw_bullets(game):
    """
    ______________________________________________________________________

    game: <Game>


    ---> None
    ______________________________________________________________________

    Draws every single bullet currently on screen.
    """
    bullets = game.bullets
    
    for bullet in bullets:

        gamelib.draw_oval(bullet.x1, bullet.y1, bullet.x2, bullet.y2, outline='', fill='#ffffff')

def draw_debug_info(game):
    """
    ______________________________________________________________________

    game: <Game>


    ---> None
    ______________________________________________________________________

    Draws debug information about the current game.
    """
    if game.show_debug_info:

        player = game.player
        cx, cy = player.center()
        debug_cons = (HEIGHT // 70)

        debug_text = f"""player_hitbox: ({player.x1}, {player.y1}), ({player.x2}, {player.y2})
center_hitbox: {(cx, cy)}
Shooting Cooldown: {'Ready!' if game.shooting_cooldown.is_zero_or_less() else game.shooting_cooldown.current_time}
Invulnerability Cooldown: {'Ready!' if game.invulnerability.is_zero_or_less() else game.invulnerability.current_time}

Power: {game.power_level}

Player Stats:
Health: {game.player.hp}
Hardness: {game.player.hardness}
Speed: {game.player.speed}

enemies_in_screen: {len(game.enemies)}
bullets_in_screen: {len(game.bullets)}"""

        gamelib.draw_text(debug_text, debug_cons, debug_cons, size=debug_cons, anchor="nw")

        if DEBUG_LINES:

            draw_debug_lines(game)

            for bullet in game.bullets:

                x, y = bullet.center()
                gamelib.draw_line(x, y - 30, x, y + 30, fill='#ff00ff')
                gamelib.draw_line(x - 30, y, x + 30, y, fill='#ff00ff')

            for enem in game.enemies:

                x, y = enem.center()
                gamelib.draw_line(x, y - 50, x, y + 50, fill='#ff00ff')
                gamelib.draw_line(x - 50, y, x + 50, y, fill='#ff00ff')

def draw_debug_lines(game):
    """
    ______________________________________________________________________

    game: <Game>


    ---> None
    ______________________________________________________________________

    Marks the limit of hitboxes and additional debug info through lines.
    """
    player = game.player
    cx, cy = player.center()

    # Upper Lines
    gamelib.draw_line(cx, 0, cx, player.y1, fill='red')
    gamelib.draw_line(cx - 5, player.y1, cx + 5, player.y1, fill='red')

    # Bottom Lines
    gamelib.draw_line(cx, player.y2, cx, HEIGHT, fill='red')
    gamelib.draw_line(cx - 5, player.y2, cx + 5, player.y2, fill='red')

    # Left Lines
    gamelib.draw_line(0, cy, player.x1, cy, fill='red')
    gamelib.draw_line(player.x1, cy - 5, player.x1, cy + 5, fill='red')

    # Right Lines
    gamelib.draw_line(player.x2, cy, WIDTH, cy, fill='red')
    gamelib.draw_line(player.x2, cy - 5, player.x2, cy + 5, fill='red')    


    # Upper-Left Corner
    gamelib.draw_line(player.x1, player.y1, player.x1 + 10, player.y1, fill='red')
    gamelib.draw_line(player.x1, player.y1, player.x1, player.y1 + 10, fill='red')

    # Upper-Right Corner
    gamelib.draw_line(player.x2, player.y1, player.x2 - 10, player.y1, fill='red')
    gamelib.draw_line(player.x2, player.y1, player.x2, player.y1 + 10, fill='red')

    # Bottom-Left Corner
    gamelib.draw_line(player.x1, player.y2, player.x1 + 10, player.y2, fill='red')
    gamelib.draw_line(player.x1, player.y2, player.x1, player.y2 - 10, fill='red')

    # Bottom-Right Corner
    gamelib.draw_line(player.x2, player.y2, player.x2 - 10, player.y2, fill='red')
    gamelib.draw_line(player.x2, player.y2, player.x2, player.y2 - 10, fill='red')

def draw_about():
    """
    ______________________________________________________________________

    ---> None
    ______________________________________________________________________

    Shows the information about the people involved in this game.
    """
    gamelib.draw_rectangle(0, 0, WIDTH, HEIGHT, width=(HEIGHT // 87), outline="#00286b", fill="#041f4d")

    gamelib.draw_text("SO, ABOUT\nTHIS GAME...", (WIDTH // 2), (HEIGHT // 6), size=(HEIGHT // 12), fill="#ffffff", justify='c')

    about_text = f"Pixel-Art:\t\t\tFranco 'NLGS' Lighterman\n\n\nCoding:\t\t\tFranco 'NLGS' Lighterman\n\n\nGamelib Library:\t\t\tDiego Essaya"

    gamelib.draw_text(about_text, (HEIGHT // 14), (HEIGHT / 2.5), size=(HEIGHT // 40), anchor="nw")

    gamelib.draw_text("Press 'RETURN' to return", (WIDTH // 2), HEIGHT - 20, size=(HEIGHT // 50), justify='c')

def draw_screen(game):
    """
    ______________________________________________________________________

    game: <Game>


    ---> None
    ______________________________________________________________________

    Draws the totality of the elements on the screen.
    """
    draw_background()
    draw_bullets(game)
    draw_debug_info(game)

    if game.is_in_game:

        draw_ship(game.player, (0 if game.invulnerability.is_zero_or_less() else 1))

        for enem in game.enemies:

            draw_ship(enem)

        draw_GUI(game)

    elif game.show_about:

        draw_about()

    else:

        draw_menus(game)