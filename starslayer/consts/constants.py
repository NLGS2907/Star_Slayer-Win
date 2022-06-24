"""
Constants Module. Contains all the constants parameters of the game.
"""

from importlib.resources import path as fpath
from typing import Optional


def abs_path(filename: str, subpackage: Optional[str]=None) -> str:
    """
    Returns the absolute path of a file associated with a package or subpackage.

    NOTE: The subpackage selected should NOT import the module this function is in.
    """

    subpackage_path = f"starslayer{f'.{subpackage}' if subpackage else ''}"

    return str(fpath(subpackage_path, filename))


GAME_VERSION = "0.2.0-alpha"
"""
The current version of the game.
"""

WIDTH = 750
"""
The width of the game window.

It is recommended to leave '750' as value.
"""

HEIGHT = 700
"""
The height of the game window.

It is recommended to leave '700' as value.
"""

GUI_SPACE = 250
"""
How much space of WIDTH the GUI will use when in-game
"""

PLAYABLE_WIDTH = WIDTH - GUI_SPACE
"""
How much space in the X axis is actually playable.
"""

CUSTOMEXT = "customppm"
"""
The custom extension to use in sprites.
"""

PROFILES_CHANGER = "Change Profile Name"
"""
Name of button that renames color profiles.
"""

PROFILES_DELETER = "Delete this Profile"
"""
Name of button that deletes the current color profile.
"""

DEFAULT_THEME = "DEFAULT"
"""
Default hidden theme that every new created theme uses as template.
"""

DEFAULT_THEME_LINES = ["...you know, don't you?",
"Nothing to see here, pal",
"The default theme is hidden, you can't use it",
"You can't use the default theme...\nYou shouldn't even know this exists",
"Did you discover this by accident? I certainly hope so",
"Waiting for a secret? Outta luck here",
"Hmmmmmmmmmmmmmmmmmmmmmmmmmm",
"(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧\n\n...happy?",
"Good try.",
"The default theme sadly is not available for the user"]
"""
Lines to say if the user tries to switch to the default theme.
"""

USED_CHEATS_LINES = ["You used cheats. As such, your score doesn't count.",
"...yeah, You used cheats. No score for you.",
"Cheaters don't deserve to be on the scoreboard.",
"Next time maybe don't use cheats."]
"""
Lines to say if the user used cheats in a run.
"""

PLAYER_HEALTH_BAR_ANIM = "player_health"
"""
Player health's animation template name.
"""

NEW_THEME = "NEW_THEME"
"""
Name template for newly created themes.
"""

EXITING_DELAY = 150
"""
How much time the game waits when the 'EXIT' action is left pressed.
"""

DEBUG_LINES = True
"""
Adds additional information on DEBUG action in process_action function (main module).
"""

SPECIAL_CHARS = '<', "/\\", "\\/", '^', 'v', '+'
"""
These chars will have their name mangled when processed.
"""

DEBUG_TEXT = """Player Hitbox: ({player_x1}, {player_y1}), ({player_x2}, {player_y2})
Hitbox Center: {hitbox_center}
Shooting Cooldown: {shooting_cooldown}
Invulnerability Cooldown: {inv_cooldown}

Real Time: {real_time}
Level: {game_level}
Power: {power_level}
Times Upgraded: {times_upgraded}

Player Stats:
Health: {health}
Hardness: {hardness}
Speed: {speed}
Ethereal: {ethereal}
Ability Gauge: {ability_gauge}

Visible on Screen:
Enemies: {enemies}
Bullets: {bullets}
Loot Drops: {drops}
"""

STAR_SLAYER_INFO = """Standard stats,
nothing special.

The same charismatic
rascal that everyone loves,
¡Now with homing bullets!


ABILITY: Shiny, terrifying,
homing bullets.
"""

BILBY_TANKA_INFO = """Slower, but has
more HP.

This tanky boy can do
something that the others
can't: AIM.


ABILITY: Orbiting bullets
shield.
"""

VIPER_DODGER_INFO = """Faster, but lower
HP.

With a little shield that
it uses to hold to its
dear life.


ABILITY: Slows god-damn
time.
"""

GAME_TITLE = """
░██████╗████████╗░█████╗░██████╗░  ░██████╗██╗░░░░░░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗  ██╔════╝██║░░░░░██╔══██╗╚██╗░██╔╝██╔════╝██╔══██╗
╚█████╗░░░░██║░░░███████║██████╔╝  ╚█████╗░██║░░░░░███████║░╚████╔╝░█████╗░░██████╔╝
░╚═══██╗░░░██║░░░██╔══██║██╔══██╗  ░╚═══██╗██║░░░░░██╔══██║░░╚██╔╝░░██╔══╝░░██╔══██╗
██████╔╝░░░██║░░░██║░░██║██║░░██║  ██████╔╝███████╗██║░░██║░░░██║░░░███████╗██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝  ╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
"""

OPTIONS_TITLE = """
░█████╗░██████╗░████████╗██╗░█████╗░███╗░░██╗░██████╗
██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔════╝
██║░░██║██████╔╝░░░██║░░░██║██║░░██║██╔██╗██║╚█████╗░
██║░░██║██╔═══╝░░░░██║░░░██║██║░░██║██║╚████║░╚═══██╗
╚█████╔╝██║░░░░░░░░██║░░░██║╚█████╔╝██║░╚███║██████╔╝
░╚════╝░╚═╝░░░░░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░
"""

CONTROLS_TITLE = """
░█████╗░░█████╗░███╗░░██╗████████╗██████╗░░█████╗░██╗░░░░░░██████╗
██╔══██╗██╔══██╗████╗░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██╔════╝
██║░░╚═╝██║░░██║██╔██╗██║░░░██║░░░██████╔╝██║░░██║██║░░░░░╚█████╗░
██║░░██╗██║░░██║██║╚████║░░░██║░░░██╔══██╗██║░░██║██║░░░░░░╚═══██╗
╚█████╔╝╚█████╔╝██║░╚███║░░░██║░░░██║░░██║╚█████╔╝███████╗██████╔╝
░╚════╝░░╚════╝░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚══════╝╚═════╝░
"""

PROFILES_TITLE = """
██████╗░██████╗░░█████╗░███████╗██╗██╗░░░░░███████╗░██████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██║██║░░░░░██╔════╝██╔════╝
██████╔╝██████╔╝██║░░██║█████╗░░██║██║░░░░░█████╗░░╚█████╗░
██╔═══╝░██╔══██╗██║░░██║██╔══╝░░██║██║░░░░░██╔══╝░░░╚═══██╗
██║░░░░░██║░░██║╚█████╔╝██║░░░░░██║███████╗███████╗██████╔╝
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░░░░╚═╝╚══════╝╚══════╝╚═════╝░
"""

CHARACTERS_TITLE = """
░█████╗░██╗░░██╗░█████╗░░█████╗░░██████╗███████╗  ░█████╗░
██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔════╝██╔════╝  ██╔══██╗
██║░░╚═╝███████║██║░░██║██║░░██║╚█████╗░█████╗░░  ███████║
██║░░██╗██╔══██║██║░░██║██║░░██║░╚═══██╗██╔══╝░░  ██╔══██║
╚█████╔╝██║░░██║╚█████╔╝╚█████╔╝██████╔╝███████╗  ██║░░██║
░╚════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═════╝░╚══════╝  ╚═╝░░╚═╝

░█████╗░██╗░░██╗░█████╗░██████╗░░█████╗░░█████╗░████████╗███████╗██████╗░
██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║░░╚═╝███████║███████║██████╔╝███████║██║░░╚═╝░░░██║░░░█████╗░░██████╔╝
██║░░██╗██╔══██║██╔══██║██╔══██╗██╔══██║██║░░██╗░░░██║░░░██╔══╝░░██╔══██╗
╚█████╔╝██║░░██║██║░░██║██║░░██║██║░░██║╚█████╔╝░░░██║░░░███████╗██║░░██║
░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
"""

GAMEOVER_TITLE = """
░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
"""

SCOREBOARD_TITLE= """
██╗░░██╗██╗░██████╗░██╗░░██╗░██████╗░█████╗░░█████╗░██████╗░███████╗░██████╗
██║░░██║██║██╔════╝░██║░░██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
███████║██║██║░░██╗░███████║╚█████╗░██║░░╚═╝██║░░██║██████╔╝█████╗░░╚█████╗░
██╔══██║██║██║░░╚██╗██╔══██║░╚═══██╗██║░░██╗██║░░██║██╔══██╗██╔══╝░░░╚═══██╗
██║░░██║██║╚██████╔╝██║░░██║██████╔╝╚█████╔╝╚█████╔╝██║░░██║███████╗██████╔╝
╚═╝░░╚═╝╚═╝░╚═════╝░╚═╝░░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░
"""

# Relative textures path
# ---------- #
## Characters
STAR_SLAYER_REL_PATH = "player/star_slayer"
BILBY_TANKA_REL_PATH = "player/bilby_tanka"
VIPER_DODGER_REL_PATH = "player/viper_dodger"
## Satellites
SHIELD_REL_PATH = "player/shield"
CANNON_REL_PATH = "player/cannon"
## Drops
MED_KIT_REL_PATH = "drops/med_kit"
RADIAL_BOMB_REL_PATH = "drops/radial_bomb"
SPIRAL_BOMB_REL_PATH = "drops/spiral_bomb"
## Enemies
ENEMY_COMMON_A_REL_PATH = "enemies/common_a"
ENEMY_COMMON_B_REL_PATH = "enemies/common_b"
ENEMY_SWIFT_REL_PATH = "enemies/swift"
# ---------- #

# Absoulte paths
# ---------- #
## Game Icon
GAME_ICON = abs_path("game_icon.gif", "textures.icon")
## Text Files
ACTIONS_PATH = abs_path("actions.json", "json.actions")
PROFILES_PATH = abs_path("color_profiles.json", "json.profiles")
SCORES_PATH = abs_path("game_scores.json", "json.scores")
LOG_PATH = abs_path("thestarthatslays.log")
## Hooks
HOOKS_GROUPS_PATH = abs_path("groups", "hooks")
## SFXs
SFX_TIME_STOP = abs_path("zawarudo.wav", "sfx.time")
SFX_TIME_CONTINUE = abs_path("soshitetokiwaugokidasu.wav", "sfx.time")
SFX_CHEAT_USED = abs_path("cheat_used.wav", "sfx.cheats")
SFX_AUDIO_ON = abs_path("audio_on.wav", "sfx.settings")
SFX_SHOOT = abs_path("shoot.wav", "sfx.gameplay")
# ---------- #
