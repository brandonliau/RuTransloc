# Standard library imports
import sys, os
from datetime import datetime
from pprint import pprint
sys.path.append(os.path.abspath('../../configuration'))
# Local imports
import config as con
import routeInfo as ri
import utils as util

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
        callName = item['call_name']
        passengerLoad = item['passenger_load']
        latitude = item['location']['lat']
        longitude = item['location']['lng']
        heading = item['heading']
        if len(item['arrival_estimates']) == 0:
            pass
        else:
            nextStop = item['arrival_estimates'][0]['stop_id']
            vehicleData.append([time, int(callName), speed, passengerLoad, int(nextStop), latitude, longitude, heading])
    return vehicleData

def getWeatherData(latitude: float, longitude: float) -> list:
    """
    :param: latitude, longitude
    :return: Relevant weather data for the given coordinates
    :usage: Processes raw weather data
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
    :return: Calculates distance to the next stop
    :usage: Uses the Pythagorean theorem to calculate distance
	"""
    stopLatitude = ri.routeMap[route][nextStop]['lat']
    stopLongitude = ri.routeMap[route][nextStop]['lng']
    finalLatitude = abs(latitude - stopLatitude)
    finalLongitude = abs(longitude - stopLongitude)
    return [((finalLatitude**2) + (finalLongitude**2))**(1/2)]

def getTrafficData(latitude: float, longitude: float) -> list:
    """
    :param: latitude, longitude
    :return: Relevant traffic data for the given coordinates
    :usage: Processes raw traffic data
	"""
    response = util.trafficAPI(latitude, longitude)
    trafficSpeed = response['flowSegmentData']['currentSpeed']
    return [trafficSpeed]

def getAgency(index: str = None):
    response = util.agencyAPI()
    i = 0
    if not index:
        for item in response['data']:
            print(f"{i} - {item['long_name']}")
            i += 1
    elif index and int(index) < len(response['data']):
        agencyID = response['data'][int(index)]['agency_id']
        print(f'Agency ID: {agencyID}')
        return agencyID
    else:
        print('Unable to retrieve agency ID for provided number')

def getRoutes(agencyID: str, index: list = None):
    response = util.routesAPI()
    agencyID = str(agencyID)
    routeDict, routes, i = {} , [], 0
    if not index:
        for item in response['data'][agencyID]:
            print(f"{i} - {item['long_name']}")
            i += 1
    elif index:
        if all(x < len(response['data'][agencyID]) for x in index):
            for x in index:
                name = response['data'][agencyID][x]['long_name'].replace(' ', '_')
                route = response['data'][agencyID][x]['route_id']
                routeDict[route] = name
                routes.append(route)
            pprint(routeDict, width = 40)
            return routes
    else:
        print('Unable to retrieve selected routes')

def getStops(agencyID: str, routes: list) -> dict:
    """
    :param: route, output (whether to print output)
    :return: All stops for the given agency
    :usage: Processes raw stop data
	"""
    response = util.stopsAPI(agencyID)
    agencyID = str(agencyID)
    stopDict = {}
    for route in routes:
        tempDict = {}
        for stop in response['data']:
            if route in stop['routes']:
                stopID = int(stop['stop_id'])
                name = stop['name']
                lat = stop['location']['lat']
                lng = stop['location']['lng']
                tempDict[stopID] = {'name': name, 'lat': lat, 'lng': lng}
        stopDict[route] = tempDict
    pprint(stopDict, width = 300)
    return stopDict
