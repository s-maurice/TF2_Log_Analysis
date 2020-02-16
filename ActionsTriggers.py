from enum import Enum


def generate_from(actions_list):
    # cant use auto() and _generate_next_value_ because the exact value needs to match the string, not the enum name
    actions_list.sort()
    for i in actions_list:
        return i.replace(" ", "_").upper() + " = '" + i + "'"


def get_actions_triggers(logs_dir="logs"):
    import os
    import re
    action_regex = '(?:\"(?:[\w ]*<\d+><\[U:1:\d+\]><(?:Red|Blue|RED|BLUE)>)\"|Team "(?:Red|Blue|RED|BLUE)"|World) ([\w ]+?) "(.+?)"'
    actions = set()
    for log_file in os.listdir(logs_dir):
        for line in open("logs/" + log_file, "r"):
            try:
                action, target = re.findall(action_regex, line)[0]
                if action == "triggered":
                    action, target = target, None
                actions.add(action)
            except IndexError:
                print("Line Unparsable:")
                print(line)
    return actions


class ActionsTriggers(Enum):
    # stores the actions/triggers found by the actions_triggers_searcher.py and stores in an enum
    GAME_OVER = 'Game_Over'
    ROUND_LENGTH = 'Round_Length'
    ROUND_START = 'Round_Start'
    ROUND_WIN = 'Round_Win'
    CAPTUREBLOCKED = 'captureblocked'
    CHANGED_ROLE_TO = 'changed role to'
    CHARGEDEPLOYED = 'chargedeployed'
    CHARGEREADY = 'chargeready'
    COMMITTED_SUICIDE_WITH = 'committed suicide with'
    CURRENT_SCORE = 'current score'
    DAMAGE = 'damage'
    DOMINATION = 'domination'
    FINAL_SCORE = 'final score'
    HEALED = 'healed'
    KILL_ASSIST = 'kill assist'
    KILLED = 'killed'
    KILLEDOBJECT = 'killedobject'
    MEDIC_DEATH = 'medic_death'
    PICKED_UP_ITEM = 'picked up item'
    PLAYER_BUILTOBJECT = 'player_builtobject'
    PLAYER_CARRYOBJECT = 'player_carryobject'
    PLAYER_DROPOBJECT = 'player_dropobject'
    PLAYER_EXTINGUISHED = 'player_extinguished'
    POINTCAPTURED = 'pointcaptured'
    REVENGE = 'revenge'
    SAY = 'say'
    SAY_TEAM = 'say_team'
    SHOT_FIRED = 'shot_fired'
    SHOT_HIT = 'shot_hit'
    SPAWNED_AS = 'spawned as'



