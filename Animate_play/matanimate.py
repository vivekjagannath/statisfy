import Metrica_IO as mio
import Metrica_Viz as mviz
import matplotlib.pyplot as plt
import pandas
import csv
import matplotlib.animation as animation
from IPython import display
from ast import literal_eval
from math import floor

tracking_home = pandas.read_csv('/home/vivek/statisfy/Animate_play/all_home_coords.csv')
tracking_away = pandas.read_csv('/home/vivek/statisfy/Animate_play/all_away_coords.csv')
events_df = pandas.read_csv('/home/vivek/statisfy/sample-data/data/Sample_Game_2/Sample_Game_2_RawEventsData.csv')

fig,ax = mviz.plot_pitch()
d, = ax.plot(literal_eval(tracking_home.iloc[0]['home_players_x_coord']), literal_eval(tracking_home.iloc[0]['home_players_y_coord']), 'bo')
e, = ax.plot(literal_eval(tracking_away.iloc[0]['away_players_x_coord']), literal_eval(tracking_away.iloc[0]['away_players_y_coord']), 'wo')
f, = ax.plot(tracking_home.iloc[0]['ball_x'], tracking_home.iloc[0]['ball_y'], 'ro')
time = ax.text(30, 34.5,"Hello", fontsize=15)
score = ax.text(-36, 34.5, "Blue 0 - 0 White", fontsize=15) 
commentary = ax.text(-9, -36.5, "Commentary", fontsize=10)
def animate(i):
    d.set_data(literal_eval(tracking_home.iloc[i]['home_players_x_coord']), literal_eval(tracking_home.iloc[i]['home_players_y_coord']))
    e.set_data(literal_eval(tracking_away.iloc[i]['away_players_x_coord']), literal_eval(tracking_away.iloc[i]['away_players_y_coord']))
    f.set_data(tracking_home.iloc[i]['ball_x'], tracking_home.iloc[i]['ball_y'])
    time.set_text("{0:0=2d}".format(floor(tracking_home.iloc[i]['Time [s]']/60)) + ":" + "{0:0=2d}".format(floor(tracking_home.iloc[i]['Time [s]']%60)))
    try:
        x = events_df[events_df['Start Frame']==i].index.values[0]
        commentary.set_text("{}".format(events_df.iloc[x]['From']) + " " + "{}".format(events_df.iloc[x]['Subtype']) + " " + "{}".format(events_df.iloc[x]['To']))
    except:
        pass
    score.set_text("Blue {0} - {1} White".format(tracking_home.iloc[i]['home_score'], tracking_home.iloc[i]['away_score']))
    return d, e, f,

animationhi = animation.FuncAnimation(fig, animate, frames = range(11641, 13801), interval = 40)
plt.show()
# animationhi.save('goalll.mp4', writer= 'ffmpeg')