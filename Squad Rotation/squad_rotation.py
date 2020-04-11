import json
import pandas
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt

#Taking input of team whose data is to be analysed
team = input()

#Creating dataframe of the json file whose data is to be analysed
with open('/home/vivek/football/open-data/data/matches/43/3.json') as match:
    data = json.load(match)
matches_df = pandas.json_normalize(data)
matches_df = matches_df.sort_values('match_id')

#Initialising empty lists to collect match ID and goal differences
l = []
gd_list = []

#Appending abovve lists with the relevant data
for i in range(len(matches_df)):
    if matches_df.iloc[i]['home_team.country.name'] == team or matches_df.iloc[i]['away_team.country.name'] == team:
        l.append(matches_df.iloc[i]['match_id'])
        gd_list.append(matches_df.iloc[i]['home_score'] - matches_df.iloc[i]['away_score'])

#Initialising empty dictionary and list to track sqauds per game
dict_of_changes = {}
squad_list = []

#appending the dictionary and list with the relevant data
for i in range(len(l)):
    with open('/home/vivek/football/open-data/data/events/{}.json'.format(l[i])) as events:
        data = json.load(events)
    events_of_match_df = pandas.json_normalize(data)
    if events_of_match_df.iloc[0]['possession_team.name'] != team:
        gd_list[i] = -gd_list[i]
    for j in range(2):
        if events_of_match_df.iloc[j]['team.name'] == team:
            for k in range(11):
                squad_list.append(events_of_match_df.iloc[j]['tactics.lineup'][k]['player']['name'])
    dict_of_changes[i] = squad_list
    squad_list = []

#assessing and recording the number of changes in the squad
no_of_changes_list = [0.2]
for i in range(1,len(dict_of_changes)):
    x = len(list(set(dict_of_changes[i]) - set(dict_of_changes[i-1])))
    if x == 0:
        x = 0.2
    no_of_changes_list.append(x)

adding colours for wins, loses and draws to plot in graph
graph_colours = []
for i in range(len(l)):
    if gd_list[i] < 0:
        graph_colours.append('#B22222')
    elif gd_list[i] > 0:
        graph_colours.append('#00ff7f')
    else:
        graph_colours.append('#A9A9A9')

#plotting bar graph
plt.bar(x=range(1,len(l)+1), height = no_of_changes_list, color=graph_colours)
plt.xlabel("Match number")
plt.ylabel("No. of changes")
plt.show()