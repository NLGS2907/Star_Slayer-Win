"""
Files Module. It reads (and writes) in files to define persistent
variables in the behaviour of the game.
"""

from json import load, dump

from .consts import DEFAULT_THEME, KEYS_PATH, LEVEL_PATH, PROFILES_PATH

StrDict = dict[str, str]
ProfilesDict = dict[str, StrDict]
LevelList = list[str | int]
LevelDict = dict[str, int | LevelList]

GameDict = StrDict | ProfilesDict | LevelDict


def load_json(file_name: str) -> GameDict:
    """
    Loads a JSON file into a python dictionary.
    """

    dict_to_return = {}

    with open(file_name) as file:

        dict_to_return = load(file)

    return dict_to_return


def dump_json(dump_dict: GameDict, file_name: str) -> None:
    """
    Dumps a python dictionary into a JSON file.
    """

    with open(file_name, mode='w') as file:

        dump(dump_dict, file, indent=4)


def list_actions(keys_dict: StrDict=load_json(KEYS_PATH)) -> list[str]:
    """
    Returns a list of all the actions in the keys file, without repetitions.
    """

    actions_list = []

    for action in keys_dict.values():

        if not action in actions_list:

            actions_list.append(action)

    return actions_list


def list_repeated_keys(value: str, keys_dict: StrDict=load_json(KEYS_PATH)) -> list[str]:
    """
    Given a value to search for and a dictionary (by default the one that 'map_keys' returns),
    it returns a list of all the keys that have such value.
    """

    return [key for (key, val) in keys_dict.items() if val == value]


def list_profiles(profiles_dict: ProfilesDict=load_json(PROFILES_PATH)) -> list[str]:
    """
    Returns a list of all the available color profiles titles.
    """

    return [profile for profile in profiles_dict if not profile == DEFAULT_THEME]


def list_attributes(profile_dict: StrDict) -> list[str]:
    """
    Returns a list of all of the attributes of a given color profile.
    """

    return [attribute for attribute in profile_dict]


def map_level(game_level: int) -> LevelDict:
    """
    Defines a dictionary with all the variables a level should have.
    """

    level_dict = load_json(LEVEL_PATH.format(level=game_level))
    return level_dict
