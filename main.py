import pandas as pd
import re

triggers_list = {'Round_Length', 'damage', 'domination', 'medic_death', 'Round_Start', 'Game_Over', 'Round_Win',
                 'player_dropobject', 'revenge', 'healed', 'pointcaptured', 'player_extinguished', 'player_builtobject',
                 'kill assist', 'chargeready', 'captureblocked', 'shot_fired', 'chargedeployed', 'killedobject',
                 'shot_hit', 'player_carryobject'}

log_data = open('logs/log_2469625.log', 'r')
print(log_data)

# first parse log data into df
log_df = pd.DataFrame(columns=["time", "origin", "action_type", "action" "target", "details"])

test_logs = open('logs/testlines.log', 'r')

for line in test_logs:
    # get the time
    time = line[15:23]

    # get the details from in the brackets
    details = re.findall("\((.+?)\)", line)

    # get origin and target - check if non-player origin
    # check for and find team
    team_search = re.findall('^Team "(Red|Blue)"', line[25:])
    if len(team_search) == 1:
        origin = team_search[0]
    elif line[25:30] == "World":  # check for and find world
        origin = "World"
    else:
        # get players not in brackets
        players = re.findall('\"(\w*<\d{4}><\[U:1:\d+\]><(Red|Blue)>)\"(?!\))', line)
        origin = players[0]
        if len(players) == 2:  # check if there's a target player
            target = players[1]
        else:
            target = None

    print(line[25:-1])
    print(origin)
    print("\n")
