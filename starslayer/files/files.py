"""
Files Module. It reads (and writes) in files to define persistent
variables in the behaviour of the game.
"""


from json import dump, load
from os import listdir
from os.path import isfile
from os.path import join as path_join
from os.path import splitext
from typing import Dict, List, Optional, Tuple

from ..consts import DEFAULT_THEME

StrDict = Dict[str, str]
ActionsDict = Dict[str, Dict[str, Tuple[str, ...]]]
ProfilesDict = Dict[str, StrDict]

GameDict = StrDict | ProfilesDict | ActionsDict


def load_json(file_name: str) -> GameDict:
    """
    Loads a JSON file into a python dictionary.
    """

    dict_to_return = {}

    with open(file_name, mode='r', encoding="utf-8") as file:

        dict_to_return = load(file)

    return dict_to_return


def dump_json(dump_dict: GameDict, file_name: str) -> None:
    """
    Dumps a python dictionary into a JSON file.
    """

    with open(file_name, mode='w', encoding="utf-8") as file:

        dump(dump_dict, file, indent=4)


def get_action_from_key(key: str, actions_dict: ActionsDict) -> Optional[str]:
    """
    Given a key and a dictionary of actions, it searches through
    the action dictionary to see which action it belongs to.
    """

    for action, action_dict in actions_dict.items():
        if key not in action_dict["keys"]:
            continue

        return action

    return None


def exists_key(key: str, actions_dict: ActionsDict) -> bool:
    """
    Given a key and a dictionary of actions, it checks if such a
    key exists in the dictionary.
    """

    for action_dict in actions_dict.values():
        if key in action_dict["keys"]:
            return True

    return False


def list_actions(actions_dict: ActionsDict) -> List[str]:
    """
    Returns a list of all the actions in the keys file, without repetitions.
    """

    return list(actions_dict.keys())


def list_action_keys(action: str, actions_dict: ActionsDict) -> List[str]:
    """
    Given an action value to search for and a dictionary,
    it returns a list of all the keys that have such action value.
    """

    return actions_dict[action]["keys"]


def action_description(action: str, actions_dict: ActionsDict) -> str:
    """
    Given an action value to search for and a dictionary,
    it returns the given description for that action.
    """

    desc = '\n'.join(actions_dict[action]["description"])

    return (desc if desc == '' else f'"{desc}"')


def list_profiles(profiles_dict: ProfilesDict) -> List[str]:
    """
    Returns a list of all the available color profiles titles.
    """

    return [profile for profile in profiles_dict if not profile == DEFAULT_THEME]


def list_attributes(profile_dict: StrDict) -> List[str]:
    """
    Returns a list of all of the attributes of a given color profile.
    """

    return list(profile_dict)


def check_ext(path: str, ext: str) -> bool:
    """
    Checks if a file or path file end with a certain extension.
    """

    return splitext(path)[1][1:].lower() == ext.lower()


def count_files(dir_path: str, preferred_ext: Optional[str]=None) -> List[str]:
    """
    Counts all the files that are in a directory path.

    Also, if `preferred_ext` is set, it checks if they have such extension.
    """

    files = []

    for elem in listdir(dir_path):
        fpath = path_join(dir_path, elem)
        if isfile(fpath) and (check_ext(fpath, preferred_ext) if preferred_ext else True):
            files.append(elem)

    return files
