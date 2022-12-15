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



# ['Player', 'Kills/game', 'Deaths/game', 'Assists/game', 'Win Rate', 'CSM', 'GPM', 'EXPM', 'DPM',
# 'VSM', 'Objectives Stolen', 'Games Played']


# testing
print(gameDuration)
