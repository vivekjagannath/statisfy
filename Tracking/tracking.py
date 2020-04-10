
import Metrica_IO as mio
import Metrica_Viz as mviz

datadir = "/Users/sidthakur08/ML/Code/Soccer/soccermatics-py/tracking/data"
gameid = 2

#reading event data
events = mio.read_event_data(datadir,gameid)

print(events['Type'].value_counts())

#converting the x and y coord wrt the field dimension(106,68)
events = mio.to_metric_coordinates(events)

#getting home and away events
home_events = events[events['Team']=='Home']
away_events = events[events['Team']=='Away']

#getting events with type as shots
shots = events[events['Type']=='SHOT']

#getting shots by home and away team
home_shots = home_events[home_events['Type']=='SHOT']
away_shots = away_events[away_events['Type']=='SHOT']

#getting shots resulting in goals for the home and away team
home_goals = home_shots[home_shots['Subtype'].str.contains('-GOAL')].copy()
away_goals = away_shots[away_shots['Subtype'].str.contains('-GOAL')].copy()

#getting the time at which the goal was scored in terms of minutes
home_goals['Minute'] = home_goals['Start Time [s]']/60
away_goals['Minute'] = away_goals['Start Time [s]']/60

#plotting goals scored by both the teams in two different sides
fig,ax = mviz.plot_pitch()
for h in home_goals.index:
    x = events.loc[h]['Start X']
    y = events.loc[h]['Start Y']
    end = events.loc[h][['End X','End Y']]
    start = events.loc[h][['Start X','Start Y']]
    if events.loc[h]['Period'] == 1:
        ax.plot(x,y,'ro')
        ax.annotate("",xy =end ,xytext =start,alpha = 0.6,arrowprops=dict(arrowstyle="->",color='r'))
    else:
        ax.plot(-x,-y,'ro')
        ax.annotate("",xy =-end ,xytext =-start,alpha = 0.6,arrowprops=dict(arrowstyle="->",color='r'))
for a in away_goals.index:
    x = events.loc[a]['Start X']
    y = events.loc[a]['Start Y']
    end = events.loc[a][['End X','End Y']]
    start = events.loc[a][['Start X','Start Y']]
    if events.loc[a]['Period'] == 1:
        ax.plot(x,y,'bo')
        ax.annotate("",xy =end ,xytext =start,alpha = 0.6,arrowprops=dict(arrowstyle="->",color='b'))
    else:
        ax.plot(-x,-y,'bo')
        ax.annotate("",xy =-end ,xytext =-start,alpha = 0.6,arrowprops=dict(arrowstyle="->",color='b'))
fig.savefig('goalstotal.png')

#plotting the events which led to the first goal by the home team
fig,ax = mviz.plot_pitch()
ax.plot(events.loc[198]['Start X'],events.loc[198]['Start Y'],'ro')
ax.annotate("",xy = events.loc[198][['End X','End Y']],xytext = events.loc[198][['Start X','Start Y']],
            alpha = 0.6,arrowprops=dict(arrowstyle="->",color='r'))
mviz.plot_events(events.loc[190:198],indicators=['Marker','Arrow'],figax=(fig,ax),annotate=True)
fig.savefig('goal1.png')

#plotting the events which led to the first goal by the away team
fig,ax = mviz.plot_pitch()
ax.plot(events.loc[823]['Start X'],events.loc[823]['Start Y'],'bo')
ax.annotate("",xy = events.loc[823][['End X','End Y']],xytext = events.loc[823][['Start X','Start Y']],
            alpha = 0.6,arrowprops=dict(arrowstyle="->",color='b'))
mviz.plot_events(events.loc[816:823],indicators=['Marker','Arrow'],figax=(fig,ax),color='b',annotate=True)
fig.savefig('goal2.png')

#moving on to the tracking data for home and away teams
tracking_home = mio.tracking_data(datadir,gameid,'Home')
tracking_away = mio.tracking_data(datadir,gameid,'Away')

#converting the x and y coord wrt the field dimension(106,68) for home and away teams
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)

#tracking player 11 for the first 12000 frames
fig,ax = mviz.plot_pitch()
ax.plot(tracking_home['Home_11_x'].iloc[:12000],tracking_home['Home_11_y'].iloc[:12000],'r.',MarkerSize = 1)
fig.savefig('gktrack.png')

#tracking player 1 for the first 12000 frames
fig,ax = mviz.plot_pitch()
ax.plot(tracking_home['Home_1_x'].iloc[:12000],tracking_home['Home_1_y'].iloc[:12000],'b.',MarkerSize = 1)
fig.savefig('deftrack.png')

#tracking player 7 for the first 12000 frames
fig,ax = mviz.plot_pitch()
ax.plot(tracking_home['Home_7_x'].iloc[:12000],tracking_home['Home_7_y'].iloc[:12000],'k.',MarkerSize = 1)
fig.savefig('midtrack.png')

#tracking player 9 for the first 12000 frames
fig,ax = mviz.plot_pitch()
ax.plot(tracking_home['Home_9_x'].iloc[:12000],tracking_home['Home_9_y'].iloc[:12000],'r.',MarkerSize = 1)
fig.savefig('sttrack.png')


# data synced with the events data where kickoff is mentioned at 51st frame of the tracking data
fig,ax = mviz.plot_frame(tracking_home.loc[51],tracking_away.loc[51])
fig.savefig('poskickoff.png')


#position of players during goal1 by the home team
fig,ax = mviz.plot_events(events.loc[198:198],indicators = ['Marker','Arrow'])
frame = events.loc[198]['Start Frame']
fig,ax = mviz.plot_frame(tracking_home.loc[frame],tracking_away.loc[frame],figax = (fig,ax))
fig.savefig('posgoal1.png')

#position of players during goal1 by the away team
fig,ax = mviz.plot_events(events.loc[823:823],indicators = ['Marker','Arrow'],color='b')
frame = events.loc[823]['Start Frame']
fig,ax = mviz.plot_frame(tracking_home.loc[frame],tracking_away.loc[frame],figax = (fig,ax))
fig.savefig('posgoal2.png')


