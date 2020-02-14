import re
import os

# simple script for searching for the needed actions and triggers
possible_actions = {'picked up item', 'revenge', 'Round_Win', 'player_extinguished', 'spawned as', 'say',
                    'player_carryobject', 'shot_hit', 'player_builtobject', 'chargeready', 'healed', 'chargedeployed',
                    'shot_fired', 'committed suicide with', 'say_team', 'Round_Length', 'pointcaptured', 'kill assist',
                    'damage', 'killed', 'Game_Over', 'current score', 'final score', 'captureblocked', 'killedobject',
                    'Round_Start', 'domination', 'player_dropobject', 'changed role to', 'medic_death'}

actions = set()

for log_file in os.listdir("logs"):
    for line in open("logs/" + log_file, "r"):
        parsed = re.findall('(?:\"(?:[\w ]*<\d+><\[U:1:\d+\]><(?:Red|Blue|RED|BLUE)>)\"|Team "(?:Red|Blue|RED|BLUE)"|World) ([\w ]+?) "(.+?)"', line)

        # print(line[:-1])
        # print(parsed, log_file)
        # print('\n')

        action, target = parsed[0]
        if action == "triggered":
            action, target = target, None
        actions.add(action)

print(actions)