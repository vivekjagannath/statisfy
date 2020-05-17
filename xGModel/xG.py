import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import FCPython
import statsmodels.api as sm
import statsmodels.formula.api as smf
import seaborn as sns

# loading in the data
with open('/Users/sidthakur08/ML/Code/Soccer/wyscout/events/events_England.json') as f:
    data = json.load(f)
train = pd.DataFrame(data)

shots = train[train['subEventName']=='Shot']
shots_model = pd.DataFrame(columns = ['Goal','X','Y'])

# considering all the shots except headers
for i, shot in shots.iterrows():
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
        #calculating distance from the center of the goal
        shots_model.at[i,'Distance'] = np.sqrt(x**2+y**2)
        #calculating the angle of the shot from the goal posts location
        a = np.arctan(7.32*x/(x**2+y**2-(7.32/2)**2))
        if a<0:
            a = np.pi+a
        shots_model.at[i,'Angle'] = a

        shots_model.at[i,'Goal'] = 0
        for shottags in shot['tags']:
            if shottags['id']==101:
                shots_model.at[i,'Goal']=1

#creating histogram data with the location of shots and goals
H_shot = np.histogram2d(shots_model['X'],shots_model['Y'],bins=50,range=[[0,100],[0,100]])
goals_only = shots_model[shots_model['Goal']==1]
H_goal = np.histogram2d(goals_only['X'],goals_only['Y'],bins=50,range=[[0,100],[0,100]])

#plotting number of shots from different points
(fig,ax) = FCPython.createGoalMouth()
pos = ax.imshow(H_shot[0],extent=[-1,66,104,-1],aspect='auto',cmap=plt.cm.Reds)
fig.colorbar(pos,ax=ax)
plt.xlim((-1,66))
plt.ylim((-3,35))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
fig.savefig('NumberOfShots.pdf', dpi=None, bbox_inches="tight")

#Plot the number of GOALS from different points
(fig,ax) = FCPython.createGoalMouth()
pos=ax.imshow(H_goal[0], extent=[-1,66,104,-1], aspect='auto',cmap=plt.cm.Reds)
fig.colorbar(pos, ax=ax)
ax.set_title('Number of goals')
plt.xlim((-1,66))
plt.ylim((-3,35))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
fig.savefig('NumberOfGoals.pdf', dpi=None, bbox_inches="tight")

#Plot the probability of scoring from different points
(fig,ax) = FCPython.createGoalMouth()
pos=ax.imshow(H_goal[0]/H_shot[0], extent=[-1,66,104,-1], aspect='auto',cmap=plt.cm.Reds,vmin=0, vmax=0.5)
fig.colorbar(pos, ax=ax)
ax.set_title('Proportion of shots resulting in a goal')
plt.xlim((-1,66))
plt.ylim((-3,35))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
fig.savefig('ProbabilityOfScoring.pdf', dpi=None, bbox_inches="tight")

#using statsmodels to get statistical summary of the model
test_model = smf.glm(formula="Goal ~ Angle+Distance" , data=shots_model, 
                           family=sm.families.Binomial()).fit()
print(test_model.summary())

b= test_model.params
model_var = ['Angle','Distance']
#Return xG value for more general model
def calculate_xG(sh):    
   bsum=b[0]
   for i,v in enumerate(model_var):
       bsum=bsum+b[i+1]*sh[v]
   xG = 1/(1+np.exp(bsum)) 
   return xG   

#Add an xG to my dataframe
xG=shots_model.apply(calculate_xG, axis=1) 
shots_model = shots_model.assign(xG=xG)

anglePlot = sns.scatterplot(shots_model['Angle'],shots_model['xG'])
fig = anglePlot.get_figure()
fig.savefig('xGxAngle.pdf')

distPlot = sns.scatterplot(shots_model['Distance'],shots_model['xG'])
fig = distPlot.get_figure()
fig.savefig('xGxDist.pdf')

#Create a 2D map of xG
pgoal_2d=np.zeros((65,65))
for x in range(65):
    for y in range(65):
        sh=dict()
        a = np.arctan(7.32 *x /(x**2 + abs(y-65/2)**2 - (7.32/2)**2))
        if a<0:
            a = np.pi + a
        sh['Angle'] = a
        sh['Distance'] = np.sqrt(x**2 + abs(y-65/2)**2)
        sh['D2'] = x**2 + abs(y-65/2)**2
        sh['X'] = x
        sh['AX'] = x*a
        sh['X2'] = x**2
        sh['C'] = abs(y-65/2)
        sh['C2'] = (y-65/2)**2
        
        pgoal_2d[x,y] =  calculate_xG(sh)

(fig,ax) = FCPython.createGoalMouth()
pos=ax.imshow(pgoal_2d, extent=[-1,65,65,-1], aspect='auto',cmap=plt.cm.Reds,vmin=0, vmax=0.3)
fig.colorbar(pos, ax=ax)
ax.set_title('Probability of goal')
plt.xlim((0,66))
plt.ylim((-3,35))
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
fig.savefig('goalprobfor_Angle + Distance.pdf', dpi=None, bbox_inches="tight")

