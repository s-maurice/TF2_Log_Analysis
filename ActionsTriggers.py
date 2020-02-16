from enum import Enum


def generate_enum_from(actions_list):
    # cant use auto() and _generate_next_value_ because the exact value needs to match the string, not the enum name
    actions_list.sort()
    for i in actions_list:
        print(i.replace(" ", "_").upper() + " = '" + i + "'")


def get_actions_triggers(logs_dir="logs"):
    import os
    import re
    action_regex = '(?:\"(?:[\w ]*<\d+><\[U:1:\d+\]><(?:Red|Blue|RED|BLUE)>)\"|Team "(?:Red|Blue|RED|BLUE)"|World) ([\w ]+?) "(.+?)"'
    action_set = set()
    for log_file in os.listdir(logs_dir):
        for line in open("logs/" + log_file, "r"):
            try:
                action, target = re.findall(action_regex, line)[0]
                if action == "triggered":
                    action, target = target, None
                action_set.add(action)
            except IndexError:
                print("Line Parse Failed:")
                print(line)
    return action_set


def get_detail_attributes(logs_dir="logs"):
    import os
    import re
    detail_regex = "\((.+?) \"(.+?)\"\)"
    detail_set = set()
    for log_file in os.listdir(logs_dir):
        for line in open("logs/" + log_file, "r"):
            details = re.findall(detail_regex, line)
            [detail_set.add(detail[0]) for detail in details]
    return detail_set


class ActionsTriggers(Enum):
    # stores the actions/triggers

    # committed suicide is converted for consistency in parsing of "with"
    # COMMITTED_SUICIDE_WITH = 'committed suicide with'  # auto generated
    COMMITTED_SUICIDE = 'committed suicide'  # manually, using if to convert during parsing instead of regex

    # auto generated
    GAME_OVER = 'Game_Over'
    ROUND_LENGTH = 'Round_Length'
    ROUND_START = 'Round_Start'
    ROUND_WIN = 'Round_Win'
    CAPTUREBLOCKED = 'captureblocked'
    CHANGED_ROLE_TO = 'changed role to'
    CHARGEDEPLOYED = 'chargedeployed'
    CHARGEREADY = 'chargeready'
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


class DetailAttributes(Enum):
    # stores the  detail names
    # TODO handle numerical positions

    # handles manually added "with" detail
    WITH = 'with'

    # auto generated
    AIRSHOT = 'airshot'
    ASSIST = 'assist'
    ASSISTER_POSITION = 'assister_position'
    ATTACKER_POSITION = 'attacker_position'
    CP = 'cp'
    CPNAME = 'cpname'
    CRIT = 'crit'
    CUSTOMKILL = 'customkill'
    DAMAGE = 'damage'
    HEADSHOT = 'headshot'
    HEALING = 'healing'
    MEDIGUN = 'medigun'
    NUMCAPPERS = 'numcappers'
    OBJECT = 'object'
    OBJECTOWNER = 'objectowner'
    PLAYER1 = 'player1'
    PLAYER2 = 'player2'
    PLAYER3 = 'player3'
    PLAYER4 = 'player4'
    PLAYER5 = 'player5'
    POSITION = 'position'
    POSITION1 = 'position1'
    POSITION2 = 'position2'
    POSITION3 = 'position3'
    POSITION4 = 'position4'
    POSITION5 = 'position5'
    REALDAMAGE = 'realdamage'
    SECONDS = 'seconds'
    UBERCHARGE = 'ubercharge'
    VICTIM_POSITION = 'victim_position'
    WEAPON = 'weapon'
    WINNER = 'winner'

