import gamelib, objects, files

WIDTH, HEIGHT = files.EXT_CONST['WIDTH'], files.EXT_CONST['HEIGHT']
GUI_SPACE = files.EXT_CONST['GUI_SPACE']
DEBUG_LINES = files.EXT_CONST['DEBUG_LINES'] # Additional information on DEBUG action.

def draw_background():
    """
    Draws the background of the game (duh).
    """
    gamelib.draw_rectangle(0, 0, WIDTH, HEIGHT, fill='#00102b')

def draw_GUI(game):
    """
    Draws the User Interface.
    """
    gamelib.draw_rectangle(WIDTH - GUI_SPACE, 0, WIDTH, HEIGHT, outline='', fill='#333333')

    gamelib.draw_text(f"Time: {game.level_timer.current_time}", (WIDTH - GUI_SPACE) + 10, 10, anchor='nw')

def draw_menus(game):
    """
    Draws in the screen the current selected menu.
    """
    menu = game.menu_in_display

    if menu.parent == None:
        gamelib.draw_text('STAR\nSLAYER', WIDTH // 2, HEIGHT // 4, size=(WIDTH // 10), justify='c')

    for button in menu.buttons_on_screen:
        gamelib.draw_rectangle(button.x1, button.y1, button.x2, button.y2, width=2, outline='#ffffff', fill='#474747', activefill='#7a7a7a')
    
        if button.msg:
            center_x, center_y = button.center()
            gamelib.draw_text(button.msg, center_x, center_y, size=16, fill='#ffffff', justify='c')


def draw_ship(ship):
    """
    Draws te sprite of a ship.
    """
    if ship.sprite == None:
        gamelib.draw_rectangle(ship.x1, ship.y1, ship.x2, ship.y2, fill='red')

    else:
        gamelib.draw_image(ship.sprite, ship.x1, ship.y1)

def draw_bullets(game):
    """
    Draws every single bullet currently on screen.
    """
    bullets = game.bullets
    
    for bullet in bullets:
        gamelib.draw_oval(bullet.x1, bullet.y1, bullet.x2, bullet.y2, fill='#ffffff', outline='')

def draw_debug_info(game):
    """
    Draws debug information about the current game.
    """
    if game.show_debug_info:
        player = game.player
        cx, cy = player.center()
        debug_cons = (HEIGHT // 70)

        debug_text = f"""player_hitbox: ({player.x1}, {player.y1}), ({player.x2}, {player.y2})
center_hitbox: {(cx, cy)}
Shooting Cooldown: {'Ready!' if game.shooting_cooldown.current_time <= 0 else game.shooting_cooldown.current_time}

Power: {game.power_level}:
Health (Player): {game.player.hp}
Hardness (Player): {game.player.hardness}
Speed (Player): {game.player.speed}

enemies_in_screen: {len(game.enemies)}
bullets_in_screen: {len(game.bullets)}"""

        gamelib.draw_text(debug_text, debug_cons, debug_cons, size=debug_cons, anchor='nw')

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

def draw_screen(game):
    """
    Draws the totality of the elements on the screen.
    """
    draw_background()
    draw_bullets(game)
    draw_debug_info(game)

    if game.is_in_game:
        draw_ship(game.player)
        for enem in game.enemies:
            draw_ship(enem)
        draw_GUI(game)
    else:
        draw_menus(game)