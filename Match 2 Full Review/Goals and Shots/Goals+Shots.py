import Metrica_IO as mio
import Metrica_Viz as mviz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv as csv

DATADIR = 'E:\Football Data\sample-data-master\data'
game_id = 2 

events = mio.read_event_data(DATADIR,game_id)

events = mio.to_metric_coordinates(events)

home_events = events[events['Team']=='Home']
away_events = events[events['Team']=='Away']

shots = events[events['Type']=='SHOT']
home_shots = home_events[home_events.Type=='SHOT']
away_shots = away_events[away_events.Type=='SHOT']

home_goals = home_shots[home_shots['Subtype'].str.contains('-GOAL')].copy()
away_goals = away_shots[away_shots['Subtype'].str.contains('-GOAL')].copy()

home_goals['Minute'] = home_goals['Start Time [s]']/60.

fig,ax = mviz.plot_pitch()
for i in home_shots.index:
    ax.plot( events.loc[i]['Start X'], events.loc[i]['Start Y'],'wo' )
    ax.annotate("", xy=events.loc[i][['End X','End Y']], xytext=events.loc[i][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='w'))
for j in home_goals.index:
    ax.plot( events.loc[j]['Start X'], events.loc[j]['Start Y'],'ro' )
    ax.annotate("", xy=events.loc[j][['End X','End Y']], xytext=events.loc[j][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='red'))
    
fig,ax = mviz.plot_pitch()
for i in away_shots.index:
    ax.plot( events.loc[i]['Start X'], events.loc[i]['Start Y'],'wo' )
    ax.annotate("", xy=events.loc[i][['End X','End Y']], xytext=events.loc[i][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='w'))
for j in away_goals.index:
    ax.plot( events.loc[j]['Start X'], events.loc[j]['Start Y'],'bo' )
    ax.annotate("", xy=events.loc[j][['End X','End Y']], xytext=events.loc[j][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='blue'))