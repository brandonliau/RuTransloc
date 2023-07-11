# Standard library imports
import sys, os
from typing import Annotated
sys.path.append(os.path.abspath('configuration'))
sys.path.append(os.path.abspath('src/tools'))
# Third party imports
from fastapi import FastAPI, Query, Depends
import pandas as pd
import pickle
# Local imports
import config as con
import routeInfo as ri
import preprocess as pre
import getData as gd

def applyModel(input: list, route: str, model: str) -> int:
    model = pickle.load(open(f'src/models/{route}/{model}', 'rb'))
    prediction = model.predict(input)
    return int(prediction[0])

def generatePrediction(routes: list = None, model: str = None) -> dict:
    """
    Return schema: {routeID: {busID: [prediction, nextStop], busID: [prediction, nextStop]}, routeID: {busID: [prediction, nextStop], busID: [prediction, nextStop]}}
    """
    predictions = {}
    if routes:
        temp = []
        for key, value in ri.allRoutes.items():
            if value in routes:
                temp.append(key)
        routes = temp
        del temp
    else:
        routes = ri.chosenRoutes
    for route in routes:
        busPredictions = {}
        vehicles = gd.getVehicleData(route)
        for vehicleData in vehicles:
            nextStop = vehicleData[4]
            latitude = vehicleData[5]
            longitude = vehicleData[6]
            trafficData = gd.getTrafficData(latitude, longitude)
            weatherData = gd.getWeatherData(latitude, longitude)
            distanceData = gd.getDistance(route, nextStop, latitude, longitude)
            raw = vehicleData + trafficData + weatherData + distanceData
            processedData = [pre.processData(raw)]
            busPredictions[vehicleData[1]] = [applyModel(processedData, ri.allRoutes[route], model), ri.routeMap[route][nextStop]['name']]
        predictions[ri.allRoutes[route]] = busPredictions
    return predictions

def returnRaw(routes: list = None) -> dict:
    """
    Return schema: {routeID: {busID: [data], busID: [data]}, routeID: {busID: [data], {busID: [data]}}}
    data = ['Time', 'Call_name', 'Speed', 'Passenger_load', 'Next_stop', 'Latitude', 'Longitude', 'Heading', 'Traffic_speed', 'Temperature', 'Windspeed', 'Precipitation', 'Humidity', 'Visibility', 'Stop_distance']
    """
    rawData = {}
    if routes:
        temp = []
        for key, value in ri.allRoutes.items():
            if value in routes:
                temp.append(key)
        routes = temp
        del temp
    else:
        routes = ri.chosenRoutes
    for route in routes:
        temp = {}
        vehicles = gd.getVehicleData(route)
        for vehicleData in vehicles:
            nextStop = vehicleData[4]
            latitude = vehicleData[5]
            longitude = vehicleData[6]
            trafficData = gd.getTrafficData(latitude, longitude)
            weatherData = gd.getWeatherData(latitude, longitude)
            distanceData = gd.getDistance(route, nextStop, latitude, longitude)
            raw = vehicleData + trafficData + weatherData + distanceData
            temp[vehicleData[1]] = raw
        rawData[ri.allRoutes[route]] = temp
    return rawData

def parseQuery(input: str) -> list:
    return input.split(',')


app = FastAPI()
@app.get('/')
async def status():
    return {'Status': 'Operational', 'Version': 'v1'}

@app.get('/predict')
async def predict(model: str = 'RandomForest'):
    return generatePrediction(model = model)

@app.get('/predict/')
async def predict(routes: str, model: str = 'RandomForest'):
    routes = parseQuery(routes)
    print(model)
    return generatePrediction(routes, model)
    
@app.get('/raw')
async def raw():
    return returnRaw()

@app.get('/raw/')
async def raw(routes: str):
    routes = parseQuery(routes)
    return returnRaw(routes)

## To be implemented ##
# @app.get('/predict/{bus}') 
# async def busPredict(bus: int):
#     return

# @app.get('/raw/{bus}')
# async def busRaw(bus: int):
#     return