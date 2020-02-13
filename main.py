import pandas as pd
import re

triggers_list = {'Round_Length', 'damage', 'domination', 'medic_death', 'Round_Start', 'Game_Over', 'Round_Win',
                 'player_dropobject', 'revenge', 'healed', 'pointcaptured', 'player_extinguished', 'player_builtobject',
                 'kill assist', 'chargeready', 'captureblocked', 'shot_fired', 'chargedeployed', 'killedobject',
                 'shot_hit', 'player_carryobject'}

log_data = open('logs/log_2469625.log', 'r')
print(log_data)

# first parse log data into df
log_df = pd.DataFrame(columns=["time", "origin", "action_target", "action", "details"])

test_logs = open('logs/testlines.log', 'r')

for line in test_logs:
    # get the time
    time = line[15:23]

    # get the details from in the brackets
    details = re.findall("\((.+?) \"(.+?)\"\)", line)

    # get origin - check if non-player origin
    # check for and find team
    team_search = re.findall('^Team "(Red|Blue)"', line[25:])
    if len(team_search) == 1:
        origin = team_search[0]
    elif line[25:30] == "World":  # check for and find world
        origin = "World"
    else:
        # get origin player
        origin = re.findall(': "(\w*)<(\d{4})><\[(U:1:\d+?)\]><(Red|Blue)>"', line)[0]

    # get action and action target
    action, target = re.findall('(?:\"(?:\w*<\d{4}><\[U:1:\d+\]><(?:Red|Blue)>)\"|Team "(?:Red|Blue)"|World) ([\w ]+?) "(\S+?)"', line)[0]
    # attempt to parse target as player
    target_player_list = re.findall('(\w*)<(\d{4})><\[(U:1:\d+?)\]><(Red|Blue)>', target)
    if len(target_player_list) > 0:
        target = target_player_list[0]
    # check if action is trigger type
    if action == "triggered":
        action, target = target, None
        # attempt to parse triggered against
        trigger_against_list = re.findall('(?:\"(?:\w*<\d{4}><\[U:1:\d+\]><(?:Red|Blue)>)\"|Team "(?:Red|Blue)"|World) triggered "(\S+?)" against "(\w*)<(\d{4})><\[(U:1:\d+?)\]><(Red|Blue)>"', line)
        if len(trigger_against_list) > 0:
            action = trigger_against_list[0][0]
            target = trigger_against_list[0][1:]

    # all details parsed - now get statistics
    print(line[25:-1])
    print(time)
    print(origin)
    print(action)
    print(target)
    print(details)
    print("\n")
