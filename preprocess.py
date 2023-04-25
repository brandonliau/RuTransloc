from collections import defaultdict
import pandas as pd
import numpy as np

def convertTime(input):
    df = input.copy()
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time'] = df['Time'].dt.tz_convert('US/Eastern')
    return df

def encodeTime(input, days):
    df = input.copy()
    df.insert(0, 'Day_sin', np.sin(2 * np.pi * df['Time'].dt.dayofweek / days))
    df.insert(1, 'Day_cos', np.cos(2 * np.pi * df['Time'].dt.dayofweek / days))
    df.insert(2, 'Hour', df['Time'].dt.hour)
    df.insert(3, 'Minute', df['Time'].dt.minute)
    df.insert(4, 'Second', df['Time'].dt.second)
    df = df.drop('Time', axis=1)
    return df

def calculateETA(input):
    df = input.copy()
    df['Which_stop'], df['ETA'] = 0, 0
    tempDict = {} # {v1ID: [Next_stop, Time, count], v2ID: [Next_stop, Time, count], ...}
    timeAtStop = defaultdict(list) # {v1ID: [arr1, arr2, arr3], V2ID: [arr1, arr2, arr3], ...}
    for i in range(len(df)):
        vehicleID = df.loc[i, 'Vehicle_id']
        nextStop = df.loc[i, 'Next_stop']
        time = df.loc[i, 'Time']
        if vehicleID not in tempDict:
            tempDict[vehicleID] = [nextStop, time, 0]
        elif nextStop != tempDict[vehicleID][0]:
            timeAtStop[vehicleID].append(tempDict[vehicleID][1])
            count = tempDict[vehicleID][2]
            tempDict[vehicleID] = [nextStop, time, count]
            tempDict[vehicleID][2] += 1
            df.loc[i, 'Which_stop'] = tempDict[vehicleID][2]
        else:
            count = tempDict[vehicleID][2]
            tempDict[vehicleID] = [nextStop, time, count]
            df.loc[i, 'Which_stop'] = count
    for i in range(len(df)):
        if df.loc[i, 'Which_stop'] == len(timeAtStop[df.loc[i, 'Vehicle_id']]):
            df = df.drop(i)
    df = df.reset_index(drop=True)
    for i in range(len(df)):
        index = df.loc[i, 'Which_stop']
        vehicle = df.loc[i, 'Vehicle_id']
        stopTime = timeAtStop[vehicle][index]
        currentTime = df.loc[i, 'Time']
        timeDifference = (stopTime - currentTime).total_seconds()
        df.loc[i, 'ETA'] = timeDifference
    df = df.drop('Which_stop', axis=1)
    return df

def filterETA(input, limit):
    df = input.copy()
    for i in range(len(df)):
        if df.loc[i, 'ETA'] > limit:
            df = df.drop(i)
    df = df.reset_index(drop=True)
    return df

df = pd.read_csv('./Data/4015044.csv') # Used for debugging purposes
df = convertTime(df)
df = calculateETA(df)
df = encodeTime(df, 5)
df = filterETA(df, 5000)
df.to_csv('output.csv', encoding='utf-8', index=False)