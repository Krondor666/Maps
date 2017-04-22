
# coding: utf-8

# In[203]:

'Thanks for the help hopefully you can understand what Im doing.Im sure the early stuff is pretty inefficient, using frames and what not, so bear with the cringe'


# In[1]:

import pandas as pd  
from random import random
import numpy as np
import scipy


# In[2]:

basicmatchinfo=pd.read_csv('Basic_Match_Info_Update.csv',header=-1)
detailedgamedata=pd.read_csv('Detailed_Game_Data.csv',header=0)


# In[3]:

detailedgamedata


# In[204]:

basicmatchinfo


# In[5]:

print(len(np.unique(basicmatchinfo[9])))
print(len(np.unique(detailedgamedata['MatchID'])))
#Need to get basicmatchinfo to length 3973- so we have matches in common only.


# In[6]:

matches_unique=np.unique(detailedgamedata['MatchID']).tolist()
#list of all unique match ID's for detailedgamedata


# In[7]:

basicmatchinfo_reduced=basicmatchinfo[basicmatchinfo[9].isin(matches_unique).reset_index(drop=True)] #basic, but with shit deleted


# In[78]:

basicmatchinfo_reduced


# In[9]:

#Now, time to create a function that creates the desired matricies


#Calling dataframes by TeamName
def team_databasic(team): 
    dfbasic = basicmatchinfo_reduced.loc[(basicmatchinfo_reduced.ix[:,0] == team) |  (basicmatchinfo_reduced.ix[:,1] == team) ]
    return(dfbasic.reset_index(drop=True))

def team_datadetailed(team): 
    dfdetailed = detailedgamedata.loc[(detailedgamedata.ix[:,'Team1'] == team) |  (detailedgamedata.ix[:,'Team2'] == team) ]
    return(dfdetailed.reset_index(drop=True))
team_datadetailed('Natus Vincere')


# In[10]:

#First, try and subset data by match ID...
def ID(team):
    IDs_unique=np.unique(team_datadetailed(team)['MatchID']).tolist()
    return(IDs_unique)

#ID('NiP')

def subset(team,i):
    return(team_datadetailed(team)[team_datadetailed(team)['MatchID']==(ID(team)[i])].reset_index(drop=True))
subset('Natus Vincere',0)

#this is NA'Vis 0th game.


# In[11]:

#Making the list for each match
list0=[0,0,0,0,0]
len(list0)

def listmaker(team,i):
    
    listlist=[]
        
    listlist.append(len(subset(team,i)['ID']))
        
    if(subset(team,i).loc[:,'Team1'][0])==team:                      # [✔]
        listlist.append(subset(team,i).loc[:,'Team1'][0])    # [✔]
    if(subset(team,i).loc[:,'Team2'][0])==team:
        listlist.append(subset(team,i).loc[:,'Team2'][0])    # [✔]
            
    if(subset(team,i).loc[:,'Team1'][0])==team:
        listlist.append(subset(team,i).loc[:,'Team2'][0]) # [✔]
    if(subset(team,i).loc[:,'Team2'][0])==team:
        listlist.append(subset(team,i).loc[:,'Team1'][0] )# [✔]
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    a=subset(team,i)['Map'].tolist()
    a=a+[0]*(len(list0)-len(a))    
    
    a.extend(listlist)
    
    a.append(subset(team,i)['MatchID'][0])
    
    return(a)
        
listmaker('NiP',0)

#ayyyyy

#this makes a list which has everything we need for a certain match_ID (all maps included, ass well as empty 'slots'w)


# In[205]:

#now to loop over each list above....

def team_matrix(team):
    listoflists=[]
    for id in range(len(ID(team))):
        listoflists.append(listmaker(team,id))
        #aarray=pd.DataFrame(listoflists)
        #aarray.columns=['Map1','Map2','Map3','Map4','Map5','Best of "x"','TeamID','OpponentID','MatchID']
    if len(pd.DataFrame(listoflists).columns)==9:
        return(pd.DataFrame(data=(listoflists), columns=['Map1','Map2','Map3','Map4','Map5',
                                                         'Best of "x"','TeamID','OpponentID','MatchID']))
        
    elif len(pd.DataFrame(listoflists).columns)==10:
        return(pd.DataFrame(data=(listoflists), columns=['Map1','Map2','Map3','Map4','Map5',
                                                         'Best of "x"','TeamID','OpponentID','MatchID', 'NAN']))
    elif len(pd.DataFrame(listoflists).columns)==11:
        return(pd.DataFrame(data=(listoflists), columns=['Map1','Map2','Map3','Map4','Map5',
                                                         'Best of "x"','TeamID','OpponentID','MatchID', 'NAN','NAN2']))
    
#I'm doing all this elif shit becuase the data was dirty and some teams had random nans/ caused above functions to not work correctly
#so, this is like a temporary (bad) fix.
#team_matrix('k1ck'), 


# In[13]:

team1=detailedgamedata['Team1'].tolist()
team2=detailedgamedata['Team2'].tolist()
teams=team1+team2
teams_unique=np.unique(teams).tolist()
teams_unique


#exceptions...
list2=[ x for x in teams_unique if "?" not in x ] #'?' caused a crash

#test=['NiP','Cloud9']


# In[14]:

#for name in list2:
#    user_data = team_matrix(name)   # This will create a copy dataframe.
#    user_data.to_csv('.'.join([name,'csv']), delimiter=',', encoding='utf-8')
'Excel spreadsheet maker'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Starting Roster one now...

# In[207]:

'Time to define the above in a different way- by defining a team by roster, not org'


# I think the best thing to do fisrt is to make a list of all unique rosters...
#Can do this by partitioning the original datasets into the members only...

#Partition:
players=np.array(detailedgamedata.ix[:,[5,15,19,23,27,31,6,35,39,43,47,51]]) #all players from both teams
players1=detailedgamedata.ix[:,[15,19,23,27,31]] #team 1 players
players2=detailedgamedata.ix[:,[35,39,43,47,51]].dropna()  #was causing issues below
players1=players1.drop(players1.index[740]) #aligns this dataframe with teh above one.

players1=np.array(players1) #had some issues doing it in one step, so did this here.(I know it seems redundant)
players2=np.array(players2)
#the splitting here was done for side-1, side-2, or team-1, team-2. Bad naming, really on my part 'playersx'


print(len(players1))
print(len(players2))

print(players[741])
print(players1[740])
print(players2[740])


# In[56]:

def rowmaker(i, array):
    return(np.sort(array[i]))

#orders each row alphabetically from a chosen team (array-players1/players2) and a chosen in index(i)
#the index means I can iterate it below 
rowmaker(1, players2)
#players2


# In[208]:

#note: yes I know I should have done array_maker and array_maker2 in one go, but I couldn't get the 
#if, elif statement for 'team 1' and 'team 2' to work.

def array_maker(): #this iterates across all the rows for (rowmaker) and puts them back together
    emptylist=[]
    for i in range(len(players1)):
        emptylist.append(rowmaker(i,players1))
        dataframe=pd.DataFrame(data=(emptylist), columns=['Player1','Player2','Player3','Player4','Player5'])
        dataframe.insert(0, 'Team1', pd.DataFrame(players).ix[:,0])
    return(dataframe)
#array_maker()


# In[209]:

def array_maker2(): #this iterates across all the rows for (rowmaker) and puts them back together
    emptylist2=[]
    for i in range(len(players2)):
        emptylist2.append(rowmaker(i,players2))
        dataframe2=pd.DataFrame(data=(emptylist2), columns=['Player1','Player2','Player3','Player4','Player5'])
        dataframe2.insert(0, 'Team2', pd.DataFrame(players).ix[:,6])
    return(dataframe2)
#array_maker2()

#I would like to combine these two into a single function, but results over form atm


# In[210]:

array1=array_maker()
array2=array_maker2()


# In[214]:

combination = pd.concat([array1,array2], keys=['Team1', 'Team2']) #this form used to make unique_list easily, but wont 
#use this form later on (would like to reconstruct dataframe)
combination.drop(['Team1','Team2'], axis = 1, inplace = True, errors = 'ignore')

#Stacks each of these arrays upon each other, with relevent key


combination_unique=combination.drop_duplicates()

print(len(combination_unique))
print(len(combination))

#Duplicates deleted :many


# In[191]:

Original_frame= pd.concat([array1, array2], axis=1, join_axes=[array1.index])
Original_frame['Map']=detailedgamedata.ix[:,3]
Original_frame['Map number']=detailedgamedata.ix[:,4]
Original_frame['ID']=detailedgamedata.ix[:,2]
Original_frame

#This is a reconstruction of what I wanted from the very start...
'Use this as a functional table from which to work with, like detailedgamedatabefore-DONT CHANGE'


# In[192]:

'Below is experimenting in dictionary-CAN CHANGE'


# In[181]:

#make dictionary of rosters

from collections import defaultdict

rosters = defaultdict(list)

for i in range(len(combination_unique)):
    rosters[i].append(str(combination_unique.ix[i,1:6]))
    
#rosters exists, and contains all rosters as a string...


# In[182]:

#Do all of the original shit, replace 'team' with dictionary entry.

def team_datadetailed(roster): 
    for i in range(len(Original_frame)):
        dfdetailed = Original_frame.loc[(str(Original_frame.ix[i,1:6]) == roster) | (str(Original_frame.ix[i,8:12]) == roster)]
    return(dfdetailed.reset_index(drop=True))
#team_datadetailed(rosters[0])


# In[183]:

if str(Original_frame.ix[0,1:6])==rosters[0]:
    print('yes')
else: 
    print('no')


# In[184]:

str(Original_frame.ix[0,1:6])


# In[185]:

rosters[0]

#the key is fucking it up, but then a dicionary needs a key


# In[190]:

'Problem is that strings arent the same. You will need to make them the same,or find another solution'


# In[193]:

#--------------------------------------------------------------------------------------------------------------------


# In[199]:

combination_unique.ix[0,3]


# In[194]:

'Below try Maxs solution, if works can delete above section'


# In[215]:

#attempting to do what Max said in messenger 



# In[ ]:



