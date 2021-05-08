def map_keys(file_name='keys.txt'):
    """
    Opens `file_name` and creates a dictionary where every key is assigned
    to an action.
    """
    keys_dict = dict()
    with open(file_name) as f:
        for line in f:
            if line == '\n':
                continue

            key, action = ''.join(line.split('=')).split()
            keys_dict[key] = action

    return keys_dict

def map_level(game_level):
    """
    Defines a dictionary with all the variables a level should have.
    """
    level_dict = dict()
    current_time = -1
    with open(f"levels/level_{game_level}.txt") as f:
        for line in f:
            if line == '\n':
                continue
            
            if line[:2] == '#t':
                _, time = line.split()
                level_dict['total_time'] = int(time)

            elif line[:2] == '#l':
                _, current_time = line.split()
                level_dict[current_time] = list()

            elif line[:2] == '#s':
                ship_dict = dict()
                attributes = line.split('#s')[1].split()

                for attribute in attributes:
                    atr, val = attribute.split('-')
                    ship_dict[atr] = (None if val == '/' else int(val))
                
                level_dict[current_time].append(ship_dict)

    return level_dict

def print_keys(keys_dict, file_name='keys.txt'):
    """
    Opens `file_name` and, if existent, edits within the information of the dictionary
    of the keys. If not, it creates one instead.
    """
    with open(file_name, mode='w') as f:
        for key, value in keys_dict.items():
            f.write(f"{key} = {value}\n\n")

def ext_constants(file_name='ext_cons.txt'):
    """
    Maps the external constants that are in a designated file (`ext_cons.txt` by default),
    and creates a dictionary with the information within.
    """
    cons_dict = dict()
    with open(file_name) as f:
        for line in f:
            if line == '\n' or line.split()[0] == '#':
                continue

            constant, value = ''.join(line.split('=')).split()

            if value.isnumeric():
                value = int(value)
            elif value == 'True':
                value = True
            elif value == 'False':
                value = False

            cons_dict[constant] = value

    return cons_dict

EXT_CONST = ext_constants()