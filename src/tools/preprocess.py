# Third party imports
from collections import defaultdict
import pandas as pd
import numpy as np

def convertTime(input: pd.DataFrame) -> pd.DataFrame:
    """
    :param: input
    :return: Pandas dataframe with converted times
    :usage: Converts times in time column to EST
	"""
    df = input.copy()
    df['Time'] = pd.to_datetime(df['Time'])
    # df['Time'] = df['Time'].dt.tz_convert('US/Eastern')
    return df

def splitTime(input: pd.DataFrame,) -> pd.DataFrame:
    df = input.copy()
    df.insert(0, 'Hour', df['Time'].dt.hour)
    df.insert(1, 'Minute', df['Time'].dt.minute)
    df.insert(2, 'Second', df['Time'].dt.second)
    df = df.drop('Time', axis=1)
    return df

def encodeTime(input: pd.DataFrame, days: int) -> pd.DataFrame:
    """
    :param: input, days (number of days in a week a route is active)
    :return: Pandas dataframe with parsed data
    :usage: Encodes day using angluar distance and parses hour, minute, and second
	"""
    df = input.copy()
    df.insert(0, 'Day_sin', np.sin(2 * np.pi * df['Time'].dt.dayofweek / days))
    df.insert(1, 'Day_cos', np.cos(2 * np.pi * df['Time'].dt.dayofweek / days))
    df.insert(2, 'Hour', df['Time'].dt.hour)
    df.insert(3, 'Minute', df['Time'].dt.minute)
    df.insert(4, 'Second', df['Time'].dt.second)
    df = df.drop('Time', axis=1)
    return df

def calculateETA(input: pd.DataFrame) -> pd.DataFrame:
    """
    :param: input
    :return: Pandas dataframe with ETA data
    :usage: Calculates ETA and filters outliers
	"""
    df = input.copy()
    df['Which_stop'], df['ETA'] = 0, 0
    tempDict = {} # {v1ID: [Next_stop, Time, count], v2ID: [Next_stop, Time, count], ...}
    timeAtStop = defaultdict(list) # {v1ID: [arrival1, arrival2, arrival3], V2ID: [arrival1, arrival2, arrival3], ...}
    for i in range(len(df)):
        vehicleID = int(str(df.loc[i, 'Call_name']) + str(df.loc[i, 'Time'].day))
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
        vehicleID = int(str(df.loc[i, 'Call_name']) + str(df.loc[i, 'Time'].day))
        if df.loc[i, 'Which_stop'] == len(timeAtStop[vehicleID]):
            df = df.drop(i)
    df = df.reset_index(drop=True)
    for i in range(len(df)):
        index = df.loc[i, 'Which_stop']
        vehicleID = int(str(df.loc[i, 'Call_name']) + str(df.loc[i, 'Time'].day))
        stopTime = timeAtStop[vehicleID][index]
        currentTime = df.loc[i, 'Time']
        timeDifference = (stopTime - currentTime).total_seconds()
        df.loc[i, 'ETA'] = timeDifference
    df = df.drop('Which_stop', axis=1)
    df.to_csv('output.csv', encoding='utf-8', index=False)
    return df

def filterETA(input, limit): # Filters outliers from ETA
    df = input.copy()
    for i in range(len(df)):
        if df.loc[i, 'ETA'] > limit:
            df = df.drop(i)
    df = df.reset_index(drop=True)
    return df

def processData(input: list) -> list:
    del input[7]
    input[0] = pd.to_datetime(input[0])
    input.insert(1, input[0].hour)
    input.insert(2, input[0].minute)
    input.insert(3, input[0].second)
    del input[0]
    return input
