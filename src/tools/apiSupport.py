# Standard library imports
import sys, os
sys.path.append(os.path.abspath('../../configuration'))
import pickle
# Third party imports
import sklearn
import sklearn.ensemble
# Local imports
import routeInfo as ri
import preprocess as pre
import getData as gd

def applyModel(data: list, route: str, model: str) -> int:
    """
    :param: data, route, model (ml)
    :return: Predicted ETA for specific vehicle
    :usage: Generate a prediction from the chosen ml model
	"""
    model = pickle.load(open(f'src/models/{route}/{model}', 'rb'))
    prediction = model.predict(data)
    return int(prediction[0])

def generatePrediction(routes: list = None, model: str = None) -> dict:
    """
    :param: routes, model (ml)
    :return: JSON of releveant information
    :usage: Generate and list all predictions to be returned by the api
    Return schema: {routeID: {busID: [prediction, nextStop], busID: [prediction, nextStop]}, routeID: {busID: [prediction, nextStop], busID: [prediction, nextStop]}}
    """
    predictions = {}
    if routes:
        temp = []
        for key, value in ri.allRoutes.items():
            if value == routes:
                print(key)
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
    :param: routes
    :return: JSON of raw data used to train and generate predictions
    :usage: Return complied data
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
