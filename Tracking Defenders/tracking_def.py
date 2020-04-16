import pandas as pd
import Metrica_IO as mio
import Metrica_Viz as mviz
import matplotlib.pyplot as plt

# defining the data path and giving the gameid we need
datadir = "/Users/sidthakur08/ML/Code/Soccer/soccermatics-py/tracking/data"
gameid = 2

# reading the event and tracking data for the home and away teams
events = mio.read_event_data(datadir,gameid)
tracking_home = mio.tracking_data(datadir,gameid,'Home')
tracking_away = mio.tracking_data(datadir,gameid,'Away')

# converting into metric coordinates to plot on pitch
events = mio.to_metric_coordinates(events)
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)

# keeping a dataframe for shot and setpieces
shots = events[events['Type']=='SHOT']
set_piece = events[events['Type']=='SET PIECE']

# getting the shots resulting in goals and the ones that were off target
goals = shots[shots['Subtype'].str.contains('-GOAL')].copy()
off = shots[shots['Subtype'].str.contains('OFF')].copy()

# this way we'll get the shots that were on target but not goals
no_goals = pd.concat([shots,goals,off]).drop_duplicates(keep=False)

# taking the home and away no goals
home_nogoals = no_goals[no_goals['Team']=='Home']
away_nogoals = no_goals[no_goals['Team']=='Away']

# getting the minute when the event happened
home_nogoals['Minute'] = no_goals['Start Time [s]']/60
away_nogoals['Minute'] = no_goals['Start Time [s]']/60

# tracking the away team's events
def track_def_away(eventind,startframe):
    fig,ax = mviz.plot_pitch()
    fig,ax = mviz.plot_events(events.loc[eventind:eventind],indicators = ['Marker','Arrow'],color='b',figax = (fig,ax))
    frame = events.loc[eventind]['Start Frame']
    fig,ax = mviz.plot_frame(tracking_home.loc[frame],tracking_away.loc[frame],figax = (fig,ax))
    ax.plot(tracking_away['Away_15_x'].iloc[startframe:(startframe+1500)],tracking_away['Away_15_y'].iloc[startframe:(startframe+1500)],'r.',MarkerSize = 1)
    ax.plot(tracking_away['Away_16_x'].iloc[startframe:(startframe+1500)],tracking_away['Away_16_y'].iloc[startframe:(startframe+1500)],'b.',MarkerSize = 1)
    ax.plot(tracking_away['Away_17_x'].iloc[startframe:(startframe+1500)],tracking_away['Away_17_y'].iloc[startframe:(startframe+1500)],'y.',MarkerSize = 1)
    ax.plot(tracking_away['Away_18_x'].iloc[startframe:(startframe+1500)],tracking_away['Away_18_y'].iloc[startframe:(startframe+1500)],'k.',MarkerSize = 1)
    plt.show()
    return fig,ax

# tracking the home team's events
def track_def_home(eventind,startframe):
    fig,ax = mviz.plot_pitch()
    fig,ax = mviz.plot_events(events.loc[eventind:eventind],indicators = ['Marker','Arrow'],color='b',figax= (fig,ax))
    frame = events.loc[eventind]['Start Frame']
    fig,ax = mviz.plot_frame(tracking_home.loc[frame],tracking_away.loc[frame],figax = (fig,ax))
    ax.plot(tracking_home['Home_1_x'].iloc[startframe:(startframe+1500)],tracking_home['Home_1_y'].iloc[startframe:(startframe+1500)],'r.',MarkerSize = 1)
    ax.plot(tracking_home['Home_2_x'].iloc[startframe:(startframe+1500)],tracking_home['Home_2_y'].iloc[startframe:(startframe+1500)],'b.',MarkerSize = 1)
    ax.plot(tracking_home['Home_3_x'].iloc[startframe:(startframe+1500)],tracking_home['Home_3_y'].iloc[startframe:(startframe+1500)],'y.',MarkerSize = 1)
    ax.plot(tracking_home['Home_4_x'].iloc[startframe:(startframe+1500)],tracking_home['Home_4_y'].iloc[startframe:(startframe+1500)],'k.',MarkerSize = 1)
    plt.show()
    return fig,ax

# plotting the defenders movement after a no-goal(shot on target but not a goal)
c = 0
for i,j in zip(home_nogoals.index.values,home_nogoals['Start Frame']):
    print(i,j)
    fig,ax = track_def_home(i,j)
    c+=1
    fig.savefig('after_shot/after_shot_track_{}'.format(c))
for i,j in zip(away_nogoals.index.values,away_nogoals['Start Frame']):
    print(i,j)
    fig,ax = track_def_away(i,j)
    c+=1
    fig.savefig('after_shot/after_shot_track_{}'.format(c))

# getting the set piece information in this case a corner
corner_kick = set_piece[set_piece['Subtype'].str.contains('CORNER')]
corner_kick_home = corner_kick[corner_kick['Team'] == 'Home']
corner_kick_away = corner_kick[corner_kick['Team'] == 'Away']

# function for plotting home team set piece info
def track_def_sp_home(eventind,startframe):
    fig,ax = mviz.plot_pitch()
    frame = events.loc[eventind]['Start Frame']
    fig,ax = mviz.plot_frame(tracking_home.loc[frame],tracking_away.loc[frame],figax = (fig,ax))
    ax.plot(tracking_home['Home_1_x'].iloc[startframe:(startframe+1500)],tracking_home['Home_1_y'].iloc[startframe:(startframe+1500)],'r.',MarkerSize = 1)
    ax.plot(tracking_home['Home_2_x'].iloc[startframe:(startframe+1500)],tracking_home['Home_2_y'].iloc[startframe:(startframe+1500)],'b.',MarkerSize = 1)
    ax.plot(tracking_home['Home_3_x'].iloc[startframe:(startframe+1500)],tracking_home['Home_3_y'].iloc[startframe:(startframe+1500)],'y.',MarkerSize = 1)
    ax.plot(tracking_home['Home_4_x'].iloc[startframe:(startframe+1500)],tracking_home['Home_4_y'].iloc[startframe:(startframe+1500)],'k.',MarkerSize = 1)
    plt.show()
    return fig,ax

# function for plotting away team set piece info
def track_def_sp_away(eventind,startframe):
    fig,ax = mviz.plot_pitch()
    frame = events.loc[eventind]['Start Frame']
    fig,ax = mviz.plot_frame(tracking_home.loc[frame],tracking_away.loc[frame],figax = (fig,ax))
    ax.plot(tracking_away['Away_15_x'].iloc[startframe:(startframe+1500)],tracking_away['Away_15_y'].iloc[startframe:(startframe+1500)],'r.',MarkerSize = 1)
    ax.plot(tracking_away['Away_16_x'].iloc[startframe:(startframe+1500)],tracking_away['Away_16_y'].iloc[startframe:(startframe+1500)],'b.',MarkerSize = 1)
    ax.plot(tracking_away['Away_17_x'].iloc[startframe:(startframe+1500)],tracking_away['Away_17_y'].iloc[startframe:(startframe+1500)],'y.',MarkerSize = 1)
    ax.plot(tracking_away['Away_18_x'].iloc[startframe:(startframe+1500)],tracking_away['Away_18_y'].iloc[startframe:(startframe+1500)],'k.',MarkerSize = 1)
    plt.show()
    return fig,ax

# plotting and saving the pitch plots for every corner in the game and how the defenders positioned themselved after this event
c = 0
for i,j in zip(corner_kick_home.index.values,corner_kick_home['Start Frame']):
    print(i,j)
    fig,ax = track_def_sp_home(i,j)
    c+=1
    fig.savefig('after_sp/after_sp_track_{}'.format(c))
for i,j in zip(corner_kick_away.index.values,corner_kick_away['Start Frame']):
    print(i,j)
    fig,ax = track_def_sp_away(i,j)
    c+=1
    fig.savefig('after_sp/after_sp_track_{}'.format(c))