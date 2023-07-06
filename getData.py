import config as con
import utils as util
from datetime import datetime
from pprint import pprint

def getVehicleData(route: str) -> list:
    """
    :param: route
    :return: Relevant data for each vehicle on the given route
    :usage: Processes raw vehicle data
	"""
    response = util.vehicleAPI(route)
    data = response['data'][f'{con.agencyID}']
    vehicleData = []
    for item in data:
        time = item['last_updated_on']
        speed = item['speed']
        vehicleId = item['vehicle_id']
        passengerLoad = item['passenger_load']
        latitude = item['location']['lat']
        longitude = item['location']['lng']
        heading = item['heading']
        if len(item['arrival_estimates']) == 0:
            pass
        else:
            nextStop = item['arrival_estimates'][0]['stop_id']
            vehicleData.append([time, int(vehicleId), speed, passengerLoad, int(nextStop), latitude, longitude, heading])
    return vehicleData

def getWeatherData(latitude: float, longitude: float) -> list:
    """
    :param: latitude, longitude
    :return: Relevant weather data for the given coordinates
    :usage: Processes raw weater data
	"""
    response = util.weatherAPI(latitude, longitude)
    temperature = response['current_weather']['temperature']
    windspeed = response['current_weather']['windspeed']
    currentTime = datetime.utcnow().isoformat(timespec='hours')
    for i in range(len(response['hourly']['time'])):
        if str(currentTime) in response['hourly']['time'][i]:
            index = i
    precipitation = response['hourly']['precipitation'][index]
    humidity = response['hourly']['relativehumidity_2m'][index]
    visibility = response['hourly']['visibility'][index]
    return [temperature, windspeed, precipitation, humidity, visibility]
    
def getDistance(route: str, nextStop: str, latitude: float, longitude: float) -> list:
    """
    :param: route, nextStop, latitude, longitude
    :return: Calculates distnace to the next stop
    :usage: Uses the Pythagorean theorem to calculate distance
	"""
    stopLatitude = con.routeDict[route][nextStop]['lat']
    stopLongitude = con.routeDict[route][nextStop]['lng']
    finalLatitude = abs(latitude - stopLatitude)
    finalLongitude = abs(longitude - stopLongitude)
    return [((finalLatitude**2) + (finalLongitude**2))**(1/2)]

def getTrafficData(latitude: float, longitude: float) -> list:
    response = util.trafficAPI(latitude, longitude)
    trafficSpeed = response['flowSegmentData']['currentSpeed']
    return [trafficSpeed]

def getStops(agencyID: str, route: str) -> dict:
    """
    :param: agencyID, routeID
    :return: All stops for the given agency
    :usage: Processes raw stop data
	"""
    routeDict, tempDict = {}, {}
    response = util.stopsAPI(agencyID)
    for stop in response['data']:
        if route in stop['routes']:
            latitude = stop['location']['lat']
            longitude = stop['location']['lng']
            tempDict[int(stop['stop_id'])] = {'lat': latitude, 'lng': longitude}
    routeDict[int(route)] = tempDict
    return routeDict
