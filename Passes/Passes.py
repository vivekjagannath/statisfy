import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.path import Path
from matplotlib.patches import PathPatch
pitchLengthX=120
pitchWidthY=80
match_id_required = 7564
home_team_required ="France"
away_team_required ="Croatia"
file_name=str(match_id_required)+'.json'
import json
with open('events/'+file_name, encoding="utf8") as data_file:
    data = json.load(data_file)
from pandas.io.json import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])    
from FCPython import createPitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
for i, thepass in passes.iterrows():
    if thepass['player_name']=='Messi':
        x=thepass['location'][0]
        y=thepass['location'][1]
        passCircle=plt.Circle((x,pitchWidthY-y),2,color="blue")
        passCircle.set_alpha(.2)
        ax.add_patch(passCircle)
        dx=thepass['pass_end_location'][0]-x
        dy=thepass['pass_end_location'][1]-y
        passArrow=plt.Arrow(x,pitchWidthY-y,dx,dy,width=2,color="blue")
        ax.add_patch(passArrow)

fig.set_size_inches(10, 7)
fig.savefig('passes.pdf', dpi=100)
plt.show()       