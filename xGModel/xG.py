import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import FCPython
import statsmodels.api as sm
import statsmodels.formula.api as smf

with open('Users/sidthakur08/ML/Code/Soccer/soccermatics/Wyscout/events/events_England.json') as f:
    data = json.load(f)

train = pd.DataFrame(data)
shots = train[train['subEventName']=='Shot']
shots_model = pd.DataFrame(columns = ['Goal','X','Y'])

for i,shot in shots.iterrows():
    header = 0
    for shottags in shot['tags']:
        if shottags['id']==403: # tag id for headers
            header = 1

    if not(header):
        shots_model.at[i,'X'] = 100-shot['positions'][0]['x']
        shots_model.at[i,'Y'] = shot['positions'][0]['y']
        shots_model.at[i,'C'] = abs(shot['positions'][0]['y']-50)

        x = shots_model.at[i,'X']*105/100
        y = shots_model.at[i,'C']*65/100
        shots_model.at[i,'Distance'] = np.sqrt(x**2+y**2)
        a = np.arctan(7.32*x/(x**2+y**2-(7.32/2)**2))
        if a<0:
            a = np.pi+a
        shots_model.at[i,'Angle'] = a

        shots_model.at[i,'Goal'] = 0
        for shottags in shot['tags']:
            if shottags['id']==101:
                shots_model.at[i,'Goal']=1

H_shot = np.histogram2d(shots_model['X'],shots_model['Y'],bins=50,range=[[0,100],[0,100]])
goals_only = shots_model[shots_model['Goal']==1]
H_goal = np.histogram2d(goals_only['X'],goals_only['Y'],bins=50,range=[[0,100],[0,100]])



