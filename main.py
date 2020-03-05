import copy

import pandas as pd
import re
from TriggerStats import *
from ActionsTriggers import ActionsTriggers, DetailAttributes

# no support for tf2center logs, as extra plugins - only focus on pugchamp


def parseline(line_string):
    # possibly try to parse with single regex in the future
    # get the time
    time = line_string[15:23]

    # get the details from in the brackets
    details = dict(re.findall("\((.+?) \"(.+?)\"\)", line_string))

    # get origin - check if non-player origin
    # check for and find team
    team_search = re.findall('^Team "(Red|Blue|RED|BLUE)"', line_string[25:])
    if len(team_search) == 1:
        origin = team_search[0]
    elif line_string[25:30] == "World":  # check for and find world
        origin = "World"
    else:
        # get origin player
        origin = re.findall(': "([\w ]*)<(\d+)><\[(U:1:\d+?)\]><(Red|Blue|RED|BLUE)>"', line_string)[0]

    # get action and action target
    action, target = re.findall('(?:\"(?:[\w ]*<\d+><\[U:1:\d+\]><(?:Red|Blue|RED|BLUE)>)\"|Team "(?:Red|Blue|RED|BLUE)"|World) ([\w ]+?) "(.+?)"', line_string)[0]
    # attempt to parse target as player
    target_player_list = re.findall('([\w ]*)<(\d+)><\[(U:1:\d+?)\]><(Red|Blue|RED|BLUE)>', target)
    if len(target_player_list) > 0:
        target = target_player_list[0]
    # check if action is trigger type
    if action == "triggered":
        action, target = target, None
        # attempt to parse triggered against
        trigger_against_list = re.findall('(?:\"(?:[\w ]*<\d+><\[U:1:\d+\]><(?:Red|Blue|RED|BLUE)>)\"|Team "(?:Red|Blue|RED|BLUE)"|World) triggered "(\S+?)" against "([\w ]*)<(\d+)><\[(U:1:\d+?)\]><(Red|Blue|RED|BLUE)>"', line_string)
        if len(trigger_against_list) > 0:
            action = trigger_against_list[0][0]
            target = trigger_against_list[0][1:]
    # for "killed", "current score" actions, re-parse to get the with attribute and add to details with type "with"
    if action == "killed" or action == "current score" or action == "committed suicide with":
        # convert committed suicide with to committed suicide and then parse "with" in the same way for consistency
        if action == "committed suicide with":
            action = "committed suicide"
        details.update(re.findall('(with) "(\w*?)"', line_string))

    return time, origin, action, target, details

# pre-loop entry setup
players_trigger_stat = PlayersTriggerStat()
players_trigger_stat_list = [players_trigger_stat]

test_logs = open('logs/testlines.log', 'r')
prev_line_stats = None
for line_index, line in enumerate(test_logs):
    time, origin, action, target, details = parseline(line)
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

    # TODO replace if with func dict
    if action == ActionsTriggers.SPAWNED_AS:
        # on player spawning ticks, update the player class
        # first try to find existing player and modify
        spawner_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        # check if player is existing, if not create
        if spawner_trigger_stat is None:
            spawner_trigger_stat = PlayerTriggerStat(origin)
            current_players_trigger_stat.add_player(spawner_trigger_stat)
        # set the class and the alive status
        spawner_trigger_stat.player_class = target
        spawner_trigger_stat.alive = True

    elif action == ActionsTriggers.CHANGED_ROLE_TO:
        # ignore, because player hasn't spawned as this class yet
        pass

    elif action == ActionsTriggers.KILLED:
        # get the PlayerTriggerStat for the killer and killed from the most recent PlayersTriggerStat
        origin_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        target_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(target[2])
        target_trigger_stat.alive = False  # set target to dead
        # parse the details
        # add the position for this current tick, copy is already made for each tick
        origin_trigger_stat.set_position_by_string(details[DetailAttributes.ATTACKER_POSITION])
        target_trigger_stat.set_position_by_string(details[DetailAttributes.VICTIM_POSITION])
        weapon = details.get(DetailAttributes.WITH, "unknown")
        # construct a KillStat
        kill_stat = KillStat(origin_trigger_stat, target_trigger_stat, weapon)

    elif action == ActionsTriggers.COMMITTED_SUICIDE:
        # copy of ActionsTriggers.KILLED, except attacker and victim are the same PlayerTriggerStat
        origin_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        origin_trigger_stat.alive = False  # set player to dead
        # parse the details
        # add the position for this current tick, copy is already made for each tick
        origin_trigger_stat.set_position_by_string(details[DetailAttributes.ATTACKER_POSITION])
        weapon = details.get(DetailAttributes.WITH, "unknown")
        # construct a KillStat
        kill_stat = KillStat(origin_trigger_stat, origin_trigger_stat, weapon)

    elif action == ActionsTriggers.KILL_ASSIST:
        # kill assist lines always follow the kill lines, double check - assert target, victim pos, attacker pos
        # get origin and add location
        assister_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        assister_trigger_stat.set_position_by_string(details[DetailAttributes.ASSISTER_POSITION])
        # place into the correct KillStat
        # TODO get the KillStat and add the assist
        kill_stat = None
        kill_stat.add_assister(assister_trigger_stat)

    elif action == ActionsTriggers.SHOT_FIRED:
        pass

    elif action == ActionsTriggers.SHOT_HIT:
        pass

    elif action == ActionsTriggers.HEALED:
        # on crusaders crossbow, previous trigger is shot hit
        origin_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        target_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(target[2])
        healing = details.get(DetailAttributes.HEALING, 0)
        heal_stat = HealStat(origin_trigger_stat, target_trigger_stat, healing)
        # check if previous line_string was arrow shot_hit
        _, _, prev_action, _, prev_details = prev_line_stats
        if prev_action == ActionsTriggers.SHOT_HIT and prev_details.get("weapon") == "crusaders_crossbow":
            heal_stat.crossbow = True

    elif action == ActionsTriggers.DAMAGE:
        origin_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        target_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(target[2])
        damage = details.get(DetailAttributes.REALDAMAGE, DetailAttributes.DAMAGE)
        weapon = details.get(DetailAttributes.WEAPON)
        damage_stat = DamageStat(origin_trigger_stat, target_trigger_stat, damage, weapon)

    elif action == ActionsTriggers.POINTCAPTURED:
        pass

    elif action == ActionsTriggers.CAPTUREBLOCKED:
        pass

    elif action == ActionsTriggers.PICKED_UP_ITEM:
        origin_trigger_stat = current_players_trigger_stat.get_player_by_steam_id(origin[2])
        item_pickup_stat = ItemPickupStat(origin_trigger_stat, target)
        item_pickup_stat.healing = details.get("healing", 0)

    prev_line_stats = line_stats  # store the line as the prev line for the next pass

