import json
import pandas
from pandas.io.json import json_normalize

with open('open-data/data/matches/43/3.json') as matches:
    data = json.load(matches)
matches_df = pandas.json_normalize(data)
matches_df = matches_df.sort_values('match_id')

for i in range(len(matches_df)):
    if matches_df.iloc[i]['home_team.country.name'] == 'Portugal' and matches_df.iloc[i]['away_team.country.name'] == 'Spain':
        id = matches_df.iloc[i]['match_id']
        break

with open('/home/vivek/football/open-data/data/events/{}.json'.format(id)) as events:
    data = json.load(events)
match_events_df = pandas.json_normalize(data)
math_events_df = match_events_df.sort_values('index')

goal_indices = []
for i in range(len(match_events_df)):
    if match_events_df.iloc[i]['type.name'] == 'Shot':
        if match_events_df.iloc[i]['shot.outcome.name'] == 'Goal':
            goal_indices.append(i)

dict_of_passes = {}
passes_indices = []
for i in range(len(goal_indices)):
    play_pattern = match_events_df.iloc[goal_indices[i]]['play_pattern.name']
    possession_team = match_events_df.iloc[goal_indices[i]]['possession_team.name']
    for j in range(goal_indices[i]-1, -1, -1):
        if match_events_df.iloc[j]['play_pattern.name'] == play_pattern and match_events_df.iloc[j]['possession_team.name'] == possession_team:
            if match_events_df.iloc[j]['type.name'] == 'Pass':
                passes_indices.append(j)
        else:
            break
    dict_of_passes[i] = passes_indices
    passes_indices = []