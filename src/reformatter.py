###########################################################################
# The reformatter file formats the raw data provided by the Replay Book   #
# software made by fraxiinus. It resorts and renames the columns and then #
# categorizes them into different .csv files depending on which role each #
# individual player in a game played for their team.                      #
###########################################################################

import csv
import pandas as pd

with open('game.csv', 'r') as infile, open('arranged.csv', 'w') as outfile:
    # outfile columns
    fieldnames = ['player', 'teamPosition', 'win', 'championsKilled', 'numDeaths', 'assists', 'minionsKilled',
                  'goldEarned', 'exp', 'totalDamageDealtToChampions', 'visionScore', 'objectivesStolen']
    # writer in outfile without empty lines containing above fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, lineterminator='\n')
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the arranged rows to the new file
        writer.writerow(row)

# rename column into readable "strings"
df = pd.read_csv('arranged.csv')
df = df.set_axis(['Player', 'Games Played', 'Win Rate', 'Kills/game', 'Deaths/game', 'Assists/game', 'CSM', 'GPM',
                  'EXPM', 'DPM', 'VSM', 'Objectives Stolen'], axis=1, copy=False)
df.to_csv('arranged.csv', index=False)

# send to respective role files
# TOP
with open('arranged.csv', 'r') as arranged, open('top.csv', 'a', newline='') as top:
    rows = csv.reader(arranged)
    topRows = [row for row in rows if 'TOP' in row]
    topWriter = csv.writer(top)
    topWriter.writerows(topRows)
# replace TOP with 1 for game count
topDf = pd.read_csv('top.csv')
topDf = topDf.replace('TOP', '1')
topDf = topDf.replace('Win', '1')
topDf = topDf.replace('Fail', '0')
topDf.to_csv('top.csv', index=False)
# JUNGLE
with open('arranged.csv', 'r') as arranged, open('jungle.csv', 'a', newline='') as jungle:
    rows = csv.reader(arranged)
    jungleRows = [row for row in rows if 'JUNGLE' in row]
    jungleWriter = csv.writer(jungle)
    jungleWriter.writerows(jungleRows)
# replace JUNGLE with 1 for game count
jungleDf = pd.read_csv('jungle.csv')
jungleDf = jungleDf.replace('JUNGLE', '1')
jungleDf = jungleDf.replace('Win', '1')
jungleDf = jungleDf.replace('Fail', '0')
jungleDf.to_csv('jungle.csv', index=False)
# MID
with open('arranged.csv', 'r') as arranged, open('mid.csv', 'a', newline='') as mid:
    rows = csv.reader(arranged)
    midRows = [row for row in rows if 'MIDDLE' in row]
    midWriter = csv.writer(mid)
    midWriter.writerows(midRows)
# replace MIDDLE with 1 for game count
midDf = pd.read_csv('mid.csv')
midDf = midDf.replace('MIDDLE', '1')
midDf = midDf.replace('Win', '1')
midDf = midDf.replace('Fail', '0')
midDf.to_csv('mid.csv', index=False)
# ADC
with open('arranged.csv', 'r') as arranged, open('adc.csv', 'a', newline='') as adc:
    rows = csv.reader(arranged)
    adcRows = [row for row in rows if 'BOTTOM' in row]
    adcWriter = csv.writer(adc)
    adcWriter.writerows(adcRows)
# replace BOTTOM with 1 for game count
adcDf = pd.read_csv('adc.csv')
adcDf = adcDf.replace('BOTTOM', '1')
adcDf = adcDf.replace('Win', '1')
adcDf = adcDf.replace('Fail', '0')
adcDf.to_csv('adc.csv', index=False)
# SUPPORT
with open('arranged.csv', 'r') as arranged, open('support.csv', 'a', newline='') as support:
    rows = csv.reader(arranged)
    supportRows = [row for row in rows if 'UTILITY' in row]
    supportWriter = csv.writer(support)
    supportWriter.writerows(supportRows)
# replace UTILITY with 1 for game count
supportDf = pd.read_csv('support.csv')
supportDf = supportDf.replace('UTILITY', '1')
supportDf = supportDf.replace('Win', '1')
supportDf = supportDf.replace('Fail', '0')
supportDf.to_csv('support.csv', index=False)

