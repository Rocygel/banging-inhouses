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
# read two new rows per game
newTopRows = topDf.tail(n=2)
xTop: int = len(topDf)
# for per minute statistics
newTopRows.loc[xTop-2:xTop-2, 'CSM':'GPM'] = (newTopRows.loc[xTop-2:xTop-2, 'CSM':'GPM']/gameDuration).round(2)
newTopRows.loc[xTop-2:xTop-2, 'EXPM':'DPM'] = (newTopRows.loc[xTop-2:xTop-2, 'EXPM':'DPM']/gameDuration).round(2)
newTopRows.loc[xTop-2, 'VSM'] = (newTopRows.loc[xTop-2, 'VSM']/gameDuration).round(2)
newTopRows.loc[xTop-1, 'VSM'] = (newTopRows.loc[xTop-1, 'VSM']/gameDuration).round(2)
newTopRows.loc[xTop-1:xTop-1, 'CSM':'GPM'] = (newTopRows.loc[xTop-1:xTop-1, 'CSM':'GPM']/gameDuration).round(2)
newTopRows.loc[xTop-1:xTop-1, 'EXPM':'DPM'] = (newTopRows.loc[xTop-1:xTop-1, 'EXPM':'DPM']/gameDuration).round(2)
topDf.loc[xTop-1] = newTopRows.loc[xTop-1]
topDf.loc[xTop-2] = newTopRows.loc[xTop-2]
topDf.to_csv('top.csv', index=False)

# ['Player', 'Kills/game', 'Deaths/game', 'Assists/game', 'Win Rate', 'CSM', 'GPM', 'EXPM', 'DPM',
# 'VSM', 'Objectives Stolen', 'Games Played']

# JUNGLE
jungleDf = pd.read_csv('jungle.csv')
# read two new rows per game
newJungleRows = jungleDf.tail(n=2)
xJungle: int = len(jungleDf)
# for per minute statistics
newJungleRows.loc[xJungle-2:xJungle-2, 'CSM':'GPM'] = (newJungleRows.loc[xJungle-2:xJungle-2,
                                                       'CSM':'GPM']/gameDuration).round(2)
newJungleRows.loc[xJungle-2, 'VSM'] = (newJungleRows.loc[xJungle-2, 'VSM']/gameDuration).round(2)
newJungleRows.loc[xJungle-2:xJungle-2, 'EXPM':'DPM'] = (newJungleRows.loc[xJungle-2:xJungle-2,
                                                        'EXPM':'DPM']/gameDuration).round(2)
newJungleRows.loc[xJungle-1, 'VSM'] = (newJungleRows.loc[xJungle-1, 'VSM']/gameDuration).round(2)
newJungleRows.loc[xJungle-1:xJungle-1, 'CSM':'GPM'] = (newJungleRows.loc[xJungle-1:xJungle-1,
                                                       'CSM':'GPM']/gameDuration).round(2)
newJungleRows.loc[xJungle-1:xJungle-1, 'EXPM':'DPM'] = (newJungleRows.loc[xJungle-1:xJungle-1,
                                                        'EXPM':'DPM']/gameDuration).round(2)
jungleDf.loc[xJungle-1] = newJungleRows.loc[xJungle-1]
jungleDf.loc[xJungle-2] = newJungleRows.loc[xJungle-2]
jungleDf.to_csv('jungle.csv', index=False)
# MID
midDf = pd.read_csv('mid.csv')
# read two new rows per game
newMidRows = midDf.tail(n=2)
xMid: int = len(midDf)
# for per minute statistics
newMidRows.loc[xMid-2:xMid-2, 'CSM':'GPM'] = (newMidRows.loc[xMid-2:xMid-2, 'CSM':'GPM']/gameDuration).round(2)
newMidRows.loc[xMid-2:xMid-2, 'EXPM':'DPM'] = (newMidRows.loc[xMid-2:xMid-2, 'EXPM':'DPM']/gameDuration).round(2)
newMidRows.loc[xMid-2, 'VSM'] = (newMidRows.loc[xMid-2, 'VSM']/gameDuration).round(2)
newMidRows.loc[xMid-1, 'VSM'] = (newMidRows.loc[xMid-1, 'VSM']/gameDuration).round(2)
newMidRows.loc[xMid-1:xMid-1, 'CSM':'GPM'] = (newMidRows.loc[xMid-1:xMid-1, 'CSM':'GPM']/gameDuration).round(2)
newMidRows.loc[xMid-1:xMid-1, 'EXPM':'DPM'] = (newMidRows.loc[xMid-1:xMid-1, 'EXPM':'DPM']/gameDuration).round(2)
midDf.loc[xMid-1] = newMidRows.loc[xMid-1]
midDf.loc[xMid-2] = newMidRows.loc[xMid-2]
midDf.to_csv('mid.csv', index=False)
# ADC
adcDf = pd.read_csv('adc.csv')
# read two new rows per game
newAdcRows = adcDf.tail(n=2)
xAdc: int = len(adcDf)
# for per minute statistics
newAdcRows.loc[xAdc-2:xAdc-2, 'CSM':'GPM'] = (newAdcRows.loc[xAdc-2:xAdc-2, 'CSM':'GPM']/gameDuration).round(2)
newAdcRows.loc[xAdc-2:xAdc-2, 'EXPM':'DPM'] = (newAdcRows.loc[xAdc-2:xAdc-2, 'EXPM':'DPM']/gameDuration).round(2)
newAdcRows.loc[xAdc-2, 'VSM'] = (newAdcRows.loc[xAdc-2, 'VSM']/gameDuration).round(2)
newAdcRows.loc[xAdc-1, 'VSM'] = (newAdcRows.loc[xAdc-1, 'VSM']/gameDuration).round(2)
newAdcRows.loc[xAdc-1:xAdc-1, 'CSM':'GPM'] = (newAdcRows.loc[xAdc-1:xAdc-1, 'CSM':'GPM']/gameDuration).round(2)
newAdcRows.loc[xAdc-1:xAdc-1, 'EXPM':'DPM'] = (newAdcRows.loc[xAdc-1:xAdc-1, 'EXPM':'DPM']/gameDuration).round(2)
adcDf.loc[xAdc-1] = newAdcRows.loc[xAdc-1]
adcDf.loc[xAdc-2] = newAdcRows.loc[xAdc-2]
adcDf.to_csv('adc.csv', index=False)
# SUPPORT
supportDf = pd.read_csv('support.csv')
# read two new rows per game
newSupportRows = supportDf.tail(n=2)
xSupport: int = len(supportDf)
# for per minute statistics
newSupportRows.loc[xSupport-2:xSupport-2, 'CSM':'GPM'] = (newSupportRows.loc[xSupport-2:xSupport-2,
                                                          'CSM':'GPM']/gameDuration).round(2)
newSupportRows.loc[xSupport-2:xSupport-2, 'EXPM':'DPM'] = (newSupportRows.loc[xSupport-2:xSupport-2,
                                                           'EXPM':'DPM']/gameDuration).round(2)
newSupportRows.loc[xSupport-2, 'VSM'] = (newSupportRows.loc[xSupport-2, 'VSM']/gameDuration).round(2)
newSupportRows.loc[xSupport-1, 'VSM'] = (newSupportRows.loc[xSupport-1, 'VSM']/gameDuration).round(2)
newSupportRows.loc[xSupport-1:xSupport-1, 'CSM':'GPM'] = (newSupportRows.loc[xSupport-1:xSupport-1,
                                                          'CSM':'GPM']/gameDuration).round(2)
newSupportRows.loc[xSupport-1:xSupport-1, 'EXPM':'DPM'] = (newSupportRows.loc[xSupport-1:xSupport-1,
                                                           'EXPM':'DPM']/gameDuration).round(2)
supportDf.loc[xSupport-1] = newSupportRows.loc[xSupport-1]
supportDf.loc[xSupport-2] = newSupportRows.loc[xSupport-2]
supportDf.to_csv('support.csv', index=False)

# testing
print(gameDuration)
print(newTopRows)
print(newJungleRows)
print(newMidRows)
print(newAdcRows)
print(newSupportRows)
