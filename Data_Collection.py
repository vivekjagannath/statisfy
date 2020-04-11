import json
import pandas
from pandas.io.json import json_normalize
import glob
from flatten_json import flatten
import numpy as np

#collecting dompetitions data into a dataframe
competitions_df = pandas.read_json('/home/vivek/football/open-data/data/competitions.json')

#collecting json file paths of all matches in tournament code specified
matches_list = glob.glob('/home/vivek/football/open-data/data/matches/43/*.json')

#collecting data out of all files in the tournament in a dataframe
matches_df = pandas.DataFrame()
for i in range (len(matches_list)):
    with open(matches_list[i]) as data_file:    
        data = json.load(data_file)
    data_flattened = [flatten(d) for d in data]
    data_flattened_df = pandas.DataFrame(data_flattened)
    data_flattened_df = data_flattened_df.replace(r'\s+', np.nan, regex=True)
    matches_df = matches_df.append(data_flattened_df)
matches_df = matches_df.dropna(axis='columns')

#list containing match_id of all games in the tournament
match_id_list = matches_df['match_id']

#initialising empty dataframes for all types of events
passes_df = pandas.DataFrame()
starting_line_up_df = pandas.DataFrame()
ball_receipt_df = pandas.DataFrame()
ball_recovery_df = pandas.DataFrame()
block_df = pandas.DataFrame()
camera_on_df = pandas.DataFrame()
camera_off_df = pandas.DataFrame()
carry_df = pandas.DataFrame()
clearance_df = pandas.DataFrame()
dispossessed_df = pandas.DataFrame()
dribble_df = pandas.DataFrame()
dribbled_past_df = pandas.DataFrame()
duel_df = pandas.DataFrame()
error_df = pandas.DataFrame()
foul_committed_df = pandas.DataFrame()
foul_won_df = pandas.DataFrame()
goal_keeper_df = pandas.DataFrame()
half_end_df = pandas.DataFrame()
half_start_df = pandas.DataFrame()
injury_stoppage_df = pandas.DataFrame()
interception_df = pandas.DataFrame()
miscontrol_df = pandas.DataFrame()
pressure_df = pandas.DataFrame()
shield_df = pandas.DataFrame()
shot_df = pandas.DataFrame()
substitution_df = pandas.DataFrame()
tactical_shift_df = pandas.DataFrame()

#running through every event of every match of the tournament and appending them to the relevant dataframe
for i in range():
    with open('/home/vivek/football/open-data/data/events/{}.json'.format(match_id_list[i])) as data_file:    
        data = json.load(data_file)
    data_flattened_df = json_normalize(data)
    for j in range (len(data_flattened_df)):
        if data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Pass':
            passes_df = passes_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Starting XI':
            starting_line_up_df = starting_line_up_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Ball Receipt*':
            ball_receipt_df = ball_receipt_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Ball Recovery':
            ball_recovery_df = ball_recovery_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Block':
            block_df = block_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Camera On':
            camera_on_df = camera_on_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Camera Off':
            camera_off_df = camera_off_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Carry':
            carry_df = carry_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Clearance':
            clearance_df = clearance_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Dispossessed':
            dispossessed_df = dispossessed_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Dribble':
            dribble_df = dribble_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Dribbled Past':
            dribbled_past_df = dribbled_past_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Duel':
            duel_df = duel_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Error':
            error_df = error_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Foul Committed':
            foul_committed_df = foul_committed_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Foul Won':
            foul_won_df = foul_won_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Goal Keeper':
            goal_keeper_df = goal_keeper_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Half End':
            half_end_df = half_end_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Half Start':
            half_start_df = half_start_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Injury Stoppage':
            injury_stoppage_df = injury_stoppage_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Interception':
            interception_df = interception_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Miscontrol':
            miscontrol_df = miscontrol_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Pressure':
            pressure_df = pressure_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Shield':
            shield_df = shield_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Shot':
            shot_df = shot_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Substitution':
            substitution_df = substitution_df.append(data_flattened_df.iloc[j])
        elif data_flattened_df.loc[j, ['type.name']]['type.name'] == 'Tactical Shift':
            tactical_shift_df = tactical_shift_df.append(data_flattened_df.iloc[j])
    print(i)

#saving .csv files of all events dataframes
passes_df.to_csv('passes.csv', index = False)
starting_line_up_df.to_csv('starting_line_up.csv', index = False)
ball_receipt_df.to_csv('ball_receipt.csv', index = False)
ball_recovery_df.to_csv('ball_recovery.csv', index = False)
block_df.to_csv('block.csv', index = False)
camera_on_df.to_csv('camera_on.csv', index = False)
camera_off_df.to_csv('camera_off.csv', index = False)
carry_df.to_csv('carry.csv', index = False)
clearance_df.to_csv('clearance.csv', index = False)
dispossessed_df.to_csv('dispossessed.csv', index = False)
dribble_df.to_csv('dribble.csv', index = False)
dribbled_past_df.to_csv('dribbled_past.csv', index = False)
duel_df.to_csv('duel.csv', index = False)
error_df.to_csv('error_df.csv', index = False)
foul_committed_df.to_csv('foul_comitted.csv', index = False)
foul_won_df.to_csv('foul_won.csv', index = False)
goal_keeper_df.to_csv('goal_keeper.csv', index = False)
half_end_df.to_csv('half_end.csv', index = False)
half_start_df.to_csv('half_start.csv', index = False)
injury_stoppage_df.to_csv('injury_stoppage.csv', index = False)
interception_df.to_csv('interception.csv', index = False)
miscontrol_df.to_csv('miscontrol.csv', index = False)
pressure_df.to_csv('pressure.csv', index = False)
shield_df.to_csv('shield.csv', index = False)
shot_df.to_csv('shot.csv', index = False)
substitution_df.to_csv('substitution.csv', index = False)
tactical_shift_df.to_csv('tactical_shift.csv', index = False)