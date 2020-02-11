import pandas as pd

triggers_list = {'medic_death', 'kill assist', 'domination', 'pointcaptured', 'chargeready', 'damage', 'healed', 'chargedeployed', 'Game_Over', 'Round_Start', 'revenge', 'captureblocked', 'Round_Win', 'Round_Length', 'shot_hit', 'shot_fired'}

log_data = open('logs/log_2469569.log', 'r')
print(log_data)

# get a player list
player_list = []

triggers = []

for line in log_data:
    try:
        triggers.append(line.split('triggered "')[1].split('"')[0])
    except:
        pass

print(set(triggers))