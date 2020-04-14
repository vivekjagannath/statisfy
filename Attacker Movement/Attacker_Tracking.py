import Metrica_IO as mio
import Metrica_Viz as mviz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv as csv

DATADIR = 'E:\Football Data\sample-data-master\data'
game_id = 2 

events = mio.read_event_data(DATADIR,game_id)

print( events['Subtype'].value_counts() )
print( events['Type'].value_counts() )

events = mio.to_metric_coordinates(events)

home_events = events[events['Team']=='Home']
away_events = events[events['Team']=='Away']

home_events['Type'].value_counts()
away_events['Type'].value_counts()

shots = events[events['Type']=='SHOT']
home_shots = home_events[home_events.Type=='SHOT']
away_shots = away_events[away_events.Type=='SHOT']

home_shots['Subtype'].value_counts()
away_shots['Subtype'].value_counts()

print( home_shots['From'].value_counts() )
print( away_shots['From'].value_counts() )

home_goals = home_shots[home_shots['Subtype'].str.contains('-GOAL')].copy()
away_goals = away_shots[away_shots['Subtype'].str.contains('-GOAL')].copy()

home_goals['Minute'] = home_goals['Start Time [s]']/60.


fig,ax = mviz.plot_pitch()
ax.plot( events.loc[198]['Start X'], events.loc[198]['Start Y'], 'ro' )
ax.annotate("", xy=events.loc[198][['End X','End Y']], xytext=events.loc[198][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))

mviz.plot_events( events.loc[190:198], indicators = ['Marker','Arrow'], annotate=True )

#### TRACKING DATA ####


tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')


print( tracking_home.columns )

tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)

# Plot some player trajectories (players 11,1,2,3,4)
fig,ax = mviz.plot_pitch()
ax.plot( tracking_home['Home_10_x'].iloc[52694:53049], tracking_home['Home_10_y'].iloc[52694:53049], 'r.', MarkerSize=1)
ax.plot( tracking_home['Home_9_x'].iloc[52694:53049], tracking_home['Home_1_y'].iloc[52694:53049], 'b.', MarkerSize=1)
