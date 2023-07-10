# Standard library imports
import sys, os
from pprint import pprint
sys.path.append(os.path.abspath('configuration'))
sys.path.append(os.path.abspath('src/tools'))
# Third party imports
from fastapi import FastAPI
import pandas as pd
import pickle
# Local imports
import config as con
import routeInfo as ri
import preprocess as pre
import getData as gd

def applyModel(input: list) -> int:
    model = pickle.load(open('src/models/randomForest', 'rb'))
    prediction = model.predict(input)
    return int(prediction[0])

def generatePrediction(routes: list = None) -> dict:
    predictions = {}
    if not routes:
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
            rawData = vehicleData + trafficData + weatherData + distanceData
            processedData = [pre.processData(rawData)]
            busPredictions[vehicleData[1]] = [applyModel(processedData), ri.routeMap[route][nextStop]['name']]
        predictions[route] = busPredictions
    return predictions
# return data schema: {routeID: {busID: [eta, nextStop], busID: [eta, nextStop]}, routeID: {busID: [eta, nextStop]}}

pprint(generatePrediction())

# app = FastAPI()
# @app.get('/predict')
# async def Predict():
#     return

# @app.get('/predict/{route}')
# async def routePredict(route: str | int):
#     if route in ri.routeMap():
#         return 
    
# @app.get('/raw')
# async def raw(raw):
#     return 

# @app.get('/raw/{route}')
# async def busRaw(route: str | int):
#     return

# @app.get('/health')
# async def health():
#     return
    
# @app.get('/predict/{bus}')
# async def busPredict(bus: int):
#     return

# @app.get('/raw/{bus}')
# async def busRaw(bus: int):
#     return