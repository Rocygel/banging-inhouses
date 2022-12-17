###############################################################################################################
# The compiler file edits the sorted data from reformatter to a satisfactory level. This includes converting  #
# certain data points to be per game/minute as well as tracking games played and overall win rate of players. #
###############################################################################################################

import json
import pandas as pd

pd.set_option('display.max_columns', None)

# open json file to access game time
with open('game.json') as json_file:
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
newTopRows.loc[xTop - 2:xTop - 2, 'CSM':'GPM'] = (
            (newTopRows.loc[xTop - 2:xTop - 2, 'CSM':'GPM']) / gameDuration).round(2)
newTopRows.loc[xTop - 2:xTop - 2, 'EXPM':'DPM'] = (
            (newTopRows.loc[xTop - 2:xTop - 2, 'EXPM':'DPM']) / gameDuration).round(2)
newTopRows.loc[xTop - 2, 'VSM'] = ((newTopRows.loc[xTop - 2, 'VSM']) / gameDuration).round(2)
newTopRows.loc[xTop - 1, 'VSM'] = ((newTopRows.loc[xTop - 1, 'VSM']) / gameDuration).round(2)
newTopRows.loc[xTop - 1:xTop - 1, 'CSM':'GPM'] = (
            (newTopRows.loc[xTop - 1:xTop - 1, 'CSM':'GPM']) / gameDuration).round(2)
newTopRows.loc[xTop - 1:xTop - 1, 'EXPM':'DPM'] = (
            (newTopRows.loc[xTop - 1:xTop - 1, 'EXPM':'DPM']) / gameDuration).round(2)
topDf.loc[xTop - 1] = newTopRows.loc[xTop - 1]
topDf.loc[xTop - 2] = newTopRows.loc[xTop - 2]
# check if new players already have played: make necessary adjustments, initially set to False
player2exists = False
player1exists = False
for old in range(0, xTop - 2):
    for new in range(xTop - 2, xTop):
        if topDf.loc[old, 'Player'] == topDf.loc[new, 'Player']:
            # add new games played number
            gamesPlayed = (topDf.loc[old, 'Games Played'] + topDf.loc[new, 'Games Played'])
            # calculate new win rate
            topDf.loc[old, 'Win Rate'] = topDf.loc[old, 'Win Rate'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'Win Rate'] = (topDf.loc[old, 'Win Rate'] + topDf.loc[new, 'Win Rate']) / gamesPlayed
            # calculate average kills, deaths, assists, CSM, GPM, EXPM, DPM and VSM
            topDf.loc[old, 'Kills/game'] = topDf.loc[old, 'Kills/game'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'Kills/game'] = (topDf.loc[old, 'Kills/game'] + topDf.loc[new, 'Kills/game']) / gamesPlayed
            topDf.loc[old, 'Assists/game'] = topDf.loc[old, 'Assists/game'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'Assists/game'] = (topDf.loc[old, 'Assists/game'] + topDf.loc[new,
                                                                                         'Assists/game']) / gamesPlayed
            topDf.loc[old, 'Deaths/game'] = topDf.loc[old, 'Deaths/game'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'Deaths/game'] = (topDf.loc[old, 'Deaths/game'] + topDf.loc[new,
                                                                                       'Deaths/game']) / gamesPlayed
            topDf.loc[old, 'CSM'] = topDf.loc[old, 'CSM'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'CSM'] = (topDf.loc[old, 'CSM'] + topDf.loc[new, 'CSM']) / gamesPlayed
            topDf.loc[old, 'GPM'] = topDf.loc[old, 'GPM'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'GPM'] = (topDf.loc[old, 'GPM'] + topDf.loc[new, 'GPM']) / gamesPlayed
            topDf.loc[old, 'EXPM'] = topDf.loc[old, 'EXPM'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'EXPM'] = (topDf.loc[old, 'EXPM'] + topDf.loc[new, 'EXPM']) / gamesPlayed
            topDf.loc[old, 'DPM'] = topDf.loc[old, 'DPM'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'DPM'] = (topDf.loc[old, 'DPM'] + topDf.loc[new, 'DPM']) / gamesPlayed
            topDf.loc[old, 'VSM'] = topDf.loc[old, 'VSM'] * topDf.loc[old, 'Games Played']
            topDf.loc[old, 'VSM'] = (topDf.loc[old, 'VSM'] + topDf.loc[new, 'VSM']) / gamesPlayed
            # adjust games played
            topDf.loc[old, 'Games Played'] = gamesPlayed
            # add objectives stolen to objectives stolen
            topDf.loc[old, 'Objectives Stolen'] = (topDf.loc[old, 'Objectives Stolen'] + topDf.loc[new,
                                                                                                   'Objectives Stolen'])
            # mark booleans to know which players to delete after loop: delete player 2 first cuz indexing
            if new == xTop - 2:
                player1exists = True
            if new == xTop - 1:
                player2exists = True
# If player exists, DELETE!
if player2exists and player1exists:
    topDf.drop(labels=[xTop - 2], axis=0, inplace=True)
    topDf.drop(labels=[xTop - 1], axis=0, inplace=True)
elif player1exists and not player2exists:
    topDf.loc[xTop - 2, :] = topDf.loc[xTop - 1, :]
    topDf.drop(labels=[xTop - 2], axis=0, inplace=True)
elif player2exists and not player1exists:
    topDf.drop(labels=[xTop - 1], axis=0, inplace=True)
# yeet it to the csv!
topDf.to_csv('top.csv', index=False)

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
# check if new players already have played: make necessary adjustments, initially set to False
player2exists = False
player1exists = False
for old in range(0, xJungle - 2):
    for new in range(xJungle - 2, xJungle):
        if jungleDf.loc[old, 'Player'] == jungleDf.loc[new, 'Player']:
            # add new games played number
            gamesPlayed = (jungleDf.loc[old, 'Games Played'] + jungleDf.loc[new, 'Games Played'])
            # calculate new win rate
            jungleDf.loc[old, 'Win Rate'] = jungleDf.loc[old, 'Win Rate'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'Win Rate'] = (jungleDf.loc[old, 'Win Rate'] +
                                             jungleDf.loc[new, 'Win Rate']) / gamesPlayed
            # calculate average kills, deaths, assists, CSM, GPM, EXPM, DPM and VSM
            jungleDf.loc[old, 'Kills/game'] = jungleDf.loc[old, 'Kills/game'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'Kills/game'] = (jungleDf.loc[old, 'Kills/game'] +
                                               jungleDf.loc[new, 'Kills/game']) / gamesPlayed
            jungleDf.loc[old, 'Assists/game'] = jungleDf.loc[old, 'Assists/game'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'Assists/game'] = (jungleDf.loc[old, 'Assists/game'] +
                                                 jungleDf.loc[new, 'Assists/game']) / gamesPlayed
            jungleDf.loc[old, 'Deaths/game'] = jungleDf.loc[old, 'Deaths/game'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'Deaths/game'] = (jungleDf.loc[old, 'Deaths/game'] +
                                                jungleDf.loc[new, 'Deaths/game']) / gamesPlayed
            jungleDf.loc[old, 'CSM'] = jungleDf.loc[old, 'CSM'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'CSM'] = (jungleDf.loc[old, 'CSM'] + jungleDf.loc[new, 'CSM']) / gamesPlayed
            jungleDf.loc[old, 'GPM'] = jungleDf.loc[old, 'GPM'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'GPM'] = (jungleDf.loc[old, 'GPM'] + jungleDf.loc[new, 'GPM']) / gamesPlayed
            jungleDf.loc[old, 'EXPM'] = jungleDf.loc[old, 'EXPM'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'EXPM'] = (jungleDf.loc[old, 'EXPM'] + jungleDf.loc[new, 'EXPM']) / gamesPlayed
            jungleDf.loc[old, 'DPM'] = jungleDf.loc[old, 'DPM'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'DPM'] = (jungleDf.loc[old, 'DPM'] + jungleDf.loc[new, 'DPM']) / gamesPlayed
            jungleDf.loc[old, 'VSM'] = jungleDf.loc[old, 'VSM'] * jungleDf.loc[old, 'Games Played']
            jungleDf.loc[old, 'VSM'] = (jungleDf.loc[old, 'VSM'] + jungleDf.loc[new, 'VSM']) / gamesPlayed
            # adjust games played
            jungleDf.loc[old, 'Games Played'] = gamesPlayed
            # add objectives stolen to objectives stolen
            jungleDf.loc[old, 'Objectives Stolen'] = (jungleDf.loc[old, 'Objectives Stolen'] +
                                                      jungleDf.loc[new, 'Objectives Stolen'])
            # mark booleans to know which players to delete after loop: delete player 2 first cuz indexing
            if new == xJungle - 2:
                player1exists = True
            if new == xJungle - 1:
                player2exists = True
# If player exists, DELETE!
if player2exists and player1exists:
    jungleDf.drop(labels=[xJungle - 2], axis=0, inplace=True)
    jungleDf.drop(labels=[xJungle - 1], axis=0, inplace=True)
elif player1exists and not player2exists:
    jungleDf.loc[xJungle - 2, :] = jungleDf.loc[xJungle - 1, :]
    jungleDf.drop(labels=[xJungle - 2], axis=0, inplace=True)
elif player2exists and not player1exists:
    jungleDf.drop(labels=[xJungle - 1], axis=0, inplace=True)
# yeet it to the csv!
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
# check if new players already have played: make necessary adjustments, initially set to False
player2exists = False
player1exists = False
for old in range(0, xMid - 2):
    for new in range(xMid - 2, xMid):
        if midDf.loc[old, 'Player'] == midDf.loc[new, 'Player']:
            # add new games played number
            gamesPlayed = (midDf.loc[old, 'Games Played'] + midDf.loc[new, 'Games Played'])
            # calculate new win rate
            midDf.loc[old, 'Win Rate'] = midDf.loc[old, 'Win Rate'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'Win Rate'] = (midDf.loc[old, 'Win Rate'] + midDf.loc[new, 'Win Rate']) / gamesPlayed
            # calculate average kills, deaths, assists, CSM, GPM, EXPM, DPM and VSM
            midDf.loc[old, 'Kills/game'] = midDf.loc[old, 'Kills/game'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'Kills/game'] = (midDf.loc[old, 'Kills/game'] + midDf.loc[new, 'Kills/game']) / gamesPlayed
            midDf.loc[old, 'Assists/game'] = midDf.loc[old, 'Assists/game'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'Assists/game'] = (midDf.loc[old, 'Assists/game'] + midDf.loc[new,
                                                                                         'Assists/game']) / gamesPlayed
            midDf.loc[old, 'Deaths/game'] = midDf.loc[old, 'Deaths/game'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'Deaths/game'] = (midDf.loc[old, 'Deaths/game'] + midDf.loc[new,
                                                                                       'Deaths/game']) / gamesPlayed
            midDf.loc[old, 'CSM'] = midDf.loc[old, 'CSM'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'CSM'] = (midDf.loc[old, 'CSM'] + midDf.loc[new, 'CSM']) / gamesPlayed
            midDf.loc[old, 'GPM'] = midDf.loc[old, 'GPM'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'GPM'] = (midDf.loc[old, 'GPM'] + midDf.loc[new, 'GPM']) / gamesPlayed
            midDf.loc[old, 'EXPM'] = midDf.loc[old, 'EXPM'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'EXPM'] = (midDf.loc[old, 'EXPM'] + midDf.loc[new, 'EXPM']) / gamesPlayed
            midDf.loc[old, 'DPM'] = midDf.loc[old, 'DPM'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'DPM'] = (midDf.loc[old, 'DPM'] + midDf.loc[new, 'DPM']) / gamesPlayed
            midDf.loc[old, 'VSM'] = midDf.loc[old, 'VSM'] * midDf.loc[old, 'Games Played']
            midDf.loc[old, 'VSM'] = (midDf.loc[old, 'VSM'] + midDf.loc[new, 'VSM']) / gamesPlayed
            # adjust games played
            midDf.loc[old, 'Games Played'] = gamesPlayed
            # add objectives stolen to objectives stolen
            midDf.loc[old, 'Objectives Stolen'] = (midDf.loc[old, 'Objectives Stolen'] + midDf.loc[new,
                                                                                                   'Objectives Stolen'])
            # mark booleans to know which players to delete after loop: delete player 2 first cuz indexing
            if new == xMid - 2:
                player1exists = True
            if new == xMid - 1:
                player2exists = True
# If player exists, DELETE!
if player2exists and player1exists:
    midDf.drop(labels=[xMid - 2], axis=0, inplace=True)
    midDf.drop(labels=[xMid - 1], axis=0, inplace=True)
elif player1exists and not player2exists:
    midDf.loc[xMid - 2, :] = midDf.loc[xMid - 1, :]
    midDf.drop(labels=[xMid - 2], axis=0, inplace=True)
elif player2exists and not player1exists:
    midDf.drop(labels=[xMid - 1], axis=0, inplace=True)
# yeet it to the csv!
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
# check if new players already have played: make necessary adjustments, initially set to False
player2exists = False
player1exists = False
for old in range(0, xAdc - 2):
    for new in range(xAdc - 2, xAdc):
        if adcDf.loc[old, 'Player'] == adcDf.loc[new, 'Player']:
            # add new games played number
            gamesPlayed = (adcDf.loc[old, 'Games Played'] + adcDf.loc[new, 'Games Played'])
            # calculate new win rate
            adcDf.loc[old, 'Win Rate'] = adcDf.loc[old, 'Win Rate'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'Win Rate'] = (adcDf.loc[old, 'Win Rate'] + adcDf.loc[new, 'Win Rate']) / gamesPlayed
            # calculate average kills, deaths, assists, CSM, GPM, EXPM, DPM and VSM
            adcDf.loc[old, 'Kills/game'] = adcDf.loc[old, 'Kills/game'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'Kills/game'] = (adcDf.loc[old, 'Kills/game'] + adcDf.loc[new, 'Kills/game']) / gamesPlayed
            adcDf.loc[old, 'Assists/game'] = adcDf.loc[old, 'Assists/game'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'Assists/game'] = (adcDf.loc[old, 'Assists/game'] + adcDf.loc[new,
                                                                                         'Assists/game']) / gamesPlayed
            adcDf.loc[old, 'Deaths/game'] = adcDf.loc[old, 'Deaths/game'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'Deaths/game'] = (adcDf.loc[old, 'Deaths/game'] + adcDf.loc[new,
                                                                                       'Deaths/game']) / gamesPlayed
            adcDf.loc[old, 'CSM'] = adcDf.loc[old, 'CSM'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'CSM'] = (adcDf.loc[old, 'CSM'] + adcDf.loc[new, 'CSM']) / gamesPlayed
            adcDf.loc[old, 'GPM'] = adcDf.loc[old, 'GPM'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'GPM'] = (adcDf.loc[old, 'GPM'] + adcDf.loc[new, 'GPM']) / gamesPlayed
            adcDf.loc[old, 'EXPM'] = adcDf.loc[old, 'EXPM'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'EXPM'] = (adcDf.loc[old, 'EXPM'] + adcDf.loc[new, 'EXPM']) / gamesPlayed
            adcDf.loc[old, 'DPM'] = adcDf.loc[old, 'DPM'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'DPM'] = (adcDf.loc[old, 'DPM'] + adcDf.loc[new, 'DPM']) / gamesPlayed
            adcDf.loc[old, 'VSM'] = adcDf.loc[old, 'VSM'] * adcDf.loc[old, 'Games Played']
            adcDf.loc[old, 'VSM'] = (adcDf.loc[old, 'VSM'] + adcDf.loc[new, 'VSM']) / gamesPlayed
            # adjust games played
            adcDf.loc[old, 'Games Played'] = gamesPlayed
            # add objectives stolen to objectives stolen
            adcDf.loc[old, 'Objectives Stolen'] = (adcDf.loc[old, 'Objectives Stolen'] + adcDf.loc[new,
                                                                                                   'Objectives Stolen'])
            # mark booleans to know which players to delete after loop: delete player 2 first cuz indexing
            if new == xAdc - 2:
                player1exists = True
            if new == xAdc - 1:
                player2exists = True
# If player exists, DELETE!
if player2exists and player1exists:
    adcDf.drop(labels=[xAdc - 2], axis=0, inplace=True)
    adcDf.drop(labels=[xAdc - 1], axis=0, inplace=True)
elif player1exists and not player2exists:
    adcDf.loc[xAdc - 2, :] = adcDf.loc[xAdc - 1, :]
    adcDf.drop(labels=[xAdc - 2], axis=0, inplace=True)
elif player2exists and not player1exists:
    adcDf.drop(labels=[xAdc - 1], axis=0, inplace=True)
# yeet it to the csv!
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
# check if new players already have played: make necessary adjustments, initially set to False
player2exists = False
player1exists = False
for old in range(0, xSupport - 2):
    for new in range(xSupport - 2, xSupport):
        if supportDf.loc[old, 'Player'] == supportDf.loc[new, 'Player']:
            # add new games played number
            gamesPlayed = (supportDf.loc[old, 'Games Played'] + supportDf.loc[new, 'Games Played'])
            # calculate new win rate
            supportDf.loc[old, 'Win Rate'] = supportDf.loc[old, 'Win Rate'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'Win Rate'] = (supportDf.loc[old, 'Win Rate'] +
                                              supportDf.loc[new, 'Win Rate']) / gamesPlayed
            # calculate average kills, deaths, assists, CSM, GPM, EXPM, DPM and VSM
            supportDf.loc[old, 'Kills/game'] = supportDf.loc[old, 'Kills/game'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'Kills/game'] = (supportDf.loc[old, 'Kills/game'] +
                                                supportDf.loc[new, 'Kills/game']) / gamesPlayed
            supportDf.loc[old, 'Assists/game'] = supportDf.loc[old, 'Assists/game'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'Assists/game'] = (supportDf.loc[old, 'Assists/game'] +
                                                  supportDf.loc[new, 'Assists/game']) / gamesPlayed
            supportDf.loc[old, 'Deaths/game'] = supportDf.loc[old, 'Deaths/game'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'Deaths/game'] = (supportDf.loc[old, 'Deaths/game'] +
                                                 supportDf.loc[new, 'Deaths/game']) / gamesPlayed
            supportDf.loc[old, 'CSM'] = supportDf.loc[old, 'CSM'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'CSM'] = (supportDf.loc[old, 'CSM'] + supportDf.loc[new, 'CSM']) / gamesPlayed
            supportDf.loc[old, 'GPM'] = supportDf.loc[old, 'GPM'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'GPM'] = (supportDf.loc[old, 'GPM'] + supportDf.loc[new, 'GPM']) / gamesPlayed
            supportDf.loc[old, 'EXPM'] = supportDf.loc[old, 'EXPM'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'EXPM'] = (supportDf.loc[old, 'EXPM'] + supportDf.loc[new, 'EXPM']) / gamesPlayed
            supportDf.loc[old, 'DPM'] = supportDf.loc[old, 'DPM'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'DPM'] = (supportDf.loc[old, 'DPM'] + supportDf.loc[new, 'DPM']) / gamesPlayed
            supportDf.loc[old, 'VSM'] = supportDf.loc[old, 'VSM'] * supportDf.loc[old, 'Games Played']
            supportDf.loc[old, 'VSM'] = (supportDf.loc[old, 'VSM'] + supportDf.loc[new, 'VSM']) / gamesPlayed
            # adjust games played
            supportDf.loc[old, 'Games Played'] = gamesPlayed
            # add objectives stolen to objectives stolen
            supportDf.loc[old, 'Objectives Stolen'] = (supportDf.loc[old, 'Objectives Stolen'] +
                                                       supportDf.loc[new, 'Objectives Stolen'])
            # mark booleans to know which players to delete after loop: delete player 2 first cuz indexing
            if new == xSupport - 2:
                player1exists = True
            if new == xSupport - 1:
                player2exists = True
# If player exists, DELETE!
if player2exists and player1exists:
    supportDf.drop(labels=[xSupport - 2], axis=0, inplace=True)
    supportDf.drop(labels=[xSupport - 1], axis=0, inplace=True)
elif player1exists and not player2exists:
    supportDf.loc[xSupport - 2, :] = supportDf.loc[xSupport - 1, :]
    supportDf.drop(labels=[xSupport - 2], axis=0, inplace=True)
elif player2exists and not player1exists:
    supportDf.drop(labels=[xSupport - 1], axis=0, inplace=True)
# yeet it to the csv!
supportDf.to_csv('support.csv', index=False)
