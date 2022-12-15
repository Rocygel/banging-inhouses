###############################################################################################################
# The compiler file edits the sorted data from reformatter to a satisfactory level. This includes changing    #
# certain data points to be per game/minute as well as tracking games played and overall win rate of players. #
###############################################################################################################

import json
import csv
import pandas as pd

# open json file to access game time
with open('test1.json') as json_file:
    data = json.load(json_file)
# calculate game duration in minutes. raw in-game tracks time in milliseconds which is not very useful for stats
gameDuration = data['gameDuration']
gameDuration = gameDuration / 60000

# edit respective role files
# TOP
topDf = pd.read_csv('top.csv')
newTopRows = topDf.tail(n=2)
newTopRows['DPM'] = (newTopRows['DPM']/gameDuration)

# value=2233
# df=(df/value).round(2)

# ['Player', 'Kills/game', 'Deaths/game', 'Assists/game', 'Win Rate', 'CSM', 'GPM', 'EXPM', 'DPM',
# 'VSM', 'Objectives Stolen', 'Games Played']
# WE NEED FOR FIRST TO DIVIDE: CSM, GPM, EXPM, DPM, VSM

# testing
print(gameDuration)
print(newTopRows)
