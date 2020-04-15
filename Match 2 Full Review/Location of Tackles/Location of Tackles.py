# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:35:49 2020

@author: vedan
"""


import sys
sys.path.append('D:/Project/Metrica Data/Code')
import Metrica_IO

import Metrica_IO as mio
import Metrica_Viz as mviz

# set up initial path to data
DATADIR = 'D:/Project/Metrica Data/sample-data-master/data'
game_id = 2 # let's look at sample match 2

# read in the event data
events = mio.read_event_data(DATADIR,game_id)

# count the number of each event type in the data
print( events['Type'].value_counts() )

# Bit of housekeeping: unit conversion from metric data units to meters
events = mio.to_metric_coordinates(events)

#To get a dataframe consisting of the total tackles won in the match
tackles = events[events['Subtype']=='TACKLE-WON']

#To plot the pitch as well as the tackles
fig,ax = mviz.plot_pitch()
for i in tackles.index:
    ax.plot( events.loc[i]['Start X'], events.loc[i]['Start Y'],'wo' )