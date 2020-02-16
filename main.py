import copy

import pandas as pd
import re
from TriggerStats import *
from ActionsTriggers import ActionsTriggers, DetailAttributes

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
    details = dict(re.findall("\((.+?) \"(.+?)\"\)", line))

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
    # for "killed", "current score" actions, re-parse to get the with attribute and add to details with type "with"
    if action == "killed" or action == "current score" or action == "committed suicide with":
        # convert committed suicide with to committed suicide and then parse "with" in the same way for consistency
        if action == "committed suicide with":
            action = "committed suicide"
        details.update(re.findall('(with) "(\w*?)"', line))

    print(line[25:-1])
    print(time)
    print(origin)
    print(action)
    print(target)
    print(details)
    print("\n")
    line_stats = {"time": time, "origin": origin, "action": action, "target": target, "details": details}

    # all details parsed - now get statistics
    # for every tick, update and append the PlayersTriggerStat - remember to deep copy
    current_players_trigger_stat = copy.deepcopy(players_trigger_stat_list[-1])
    current_players_trigger_stat.clear_positions()  # remove the positions from the previous tick

    if action == ActionsTriggers.SPAWNED_AS:
        # on player spawning ticks, update the player class
        # first try to find existing player and modify
        spawner_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        # check if player is existing, if not create
        if spawner_trigger_stat is None:
            spawner_trigger_stat = PlayerTriggerStat(origin)
        # set the class which is the target
        spawner_trigger_stat.player_class = target

    elif action == ActionsTriggers.CHANGED_ROLE_TO:
        # ignore, because player hasn't spawned as this class yet
        pass

    elif action == ActionsTriggers.KILLED:
        # get the PlayerTriggerStat for the killer and killed from the most recent PlayersTriggerStat
        origin_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        target_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(target[2])
        # parse the details
        # add the position for this current tick, copy is already made for each tick
        origin_trigger_stat.set_position_by_string(details[DetailAttributes.ATTACKER_POSITION])
        target_trigger_stat.set_position_by_string(details[DetailAttributes.VICTIM_POSITION])
        weapon = details.get(DetailAttributes.WITH, "unknown")
        # construct a KillStat
        kill_stat = KillStat(origin_trigger_stat, target_trigger_stat, weapon=weapon)

    elif action == ActionsTriggers.COMMITTED_SUICIDE:
        # copy of ActionsTriggers.KILLED, except attacker and victim are the same PlayerTriggerStat
        origin_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        # parse the details
        # add the position for this current tick, copy is already made for each tick
        origin_trigger_stat.set_position_by_string(details[DetailAttributes.ATTACKER_POSITION])
        weapon = details.get(DetailAttributes.WITH, "unknown")
        # construct a KillStat
        kill_stat = KillStat(origin_trigger_stat, origin_trigger_stat, weapon=weapon)

    elif action == ActionsTriggers.KILL_ASSIST:
        # kill assist lines always follow the kill lines, double check - assert target, victim pos, attacker pos
        # get origin and add location
        assister_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        assister_trigger_stat.set_position_by_string(details[DetailAttributes.ASSISTER_POSITION])
        # place into the correct KillStat
        # TODO get the KillStat and add the assist
        kill_stat = None
        kill_stat.add_assister(assister_trigger_stat)

