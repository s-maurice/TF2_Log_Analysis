import copy

import pandas as pd
import re
from TriggerStats import *

# no support for tf2center logs, as extra plugins - only focus on pugchamp

# pre-loop entry setup
players_trigger_stat = PlayersTriggerStat()
players_trigger_stat_list = [players_trigger_stat]

test_logs = open('logs/testlines.log', 'r')
for line in test_logs:
    # possibly try to parse with single regex in the future
    # get the time
    time = line[15:23]

    # get the details from in the brackets
    details = re.findall("\((.+?) \"(.+?)\"\)", line)

    # get origin - check if non-player origin
    # check for and find team
    team_search = re.findall('^Team "(Red|Blue|RED|BLUE)"', line[25:])
    if len(team_search) == 1:
        origin = team_search[0]
    elif line[25:30] == "World":  # check for and find world
        origin = "World"
    else:
        # get origin player
        origin = re.findall(': "([\w ]*)<(\d+)><\[(U:1:\d+?)\]><(Red|Blue|RED|BLUE)>"', line)[0]

    # get action and action target
    action, target = re.findall('(?:\"(?:[\w ]*<\d+><\[U:1:\d+\]><(?:Red|Blue|RED|BLUE)>)\"|Team "(?:Red|Blue|RED|BLUE)"|World) ([\w ]+?) "(.+?)"', line)[0]
    # attempt to parse target as player
    target_player_list = re.findall('([\w ]*)<(\d+)><\[(U:1:\d+?)\]><(Red|Blue|RED|BLUE)>', target)
    if len(target_player_list) > 0:
        target = target_player_list[0]
    # check if action is trigger type
    if action == "triggered":
        action, target = target, None
        # attempt to parse triggered against
        trigger_against_list = re.findall('(?:\"(?:[\w ]*<\d+><\[U:1:\d+\]><(?:Red|Blue|RED|BLUE)>)\"|Team "(?:Red|Blue|RED|BLUE)"|World) triggered "(\S+?)" against "([\w ]*)<(\d+)><\[(U:1:\d+?)\]><(Red|Blue|RED|BLUE)>"', line)
        if len(trigger_against_list) > 0:
            action = trigger_against_list[0][0]
            target = trigger_against_list[0][1:]

    print(line[25:-1])
    print(time)
    print(origin)
    print(action)
    print(target)
    print(details)
    print("\n")
