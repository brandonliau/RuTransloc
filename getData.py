import config as con
import apiCall as api
import busStops as bs
from datetime import datetime

def getVehicleData(route):
    response = api.vehicleAPI(route)
    data = response['data'][f'{con.agencyID}']
    for item in data:
        time = item['last_updated_on']
        speed = item['speed']
        vehicleId = item['vehicle_id']
        passengerLoad = item['passenger_load']
        nextStop = item['arrival_estimates'][0]['stop_id']
        latitude = item['location']['lat']
        longitude = item['location']['lng']
        heading = item['heading']
        vehicleData = [time, speed, int(vehicleId), passengerLoad, int(nextStop), latitude, longitude, heading]
    return vehicleData

def getWeatherData(latitude, longitude):
    response = api.weatherAPI(latitude, longitude)
    temperature = response['current_weather']['temperature']
    windspeed = response['current_weather']['windspeed']
    currentTime = datetime.now().isoformat(timespec='hours')
    for i in range(len(response['hourly']['time'])):
        if str(currentTime) in response['hourly']['time'][i]:
            index = i
    precipitation = response['hourly']['precipitation'][index]
    humidity = response['hourly']['relativehumidity_2m'][index]
    visibility = response['hourly']['visibility'][index]
    return [temperature, windspeed, precipitation, humidity, visibility]
    
def getDistance(route, nextStop, latitude, longitude):
    stopLatitude = bs.stopsDict[route][nextStop]['lat']
    stopLongitude = bs.stopsDict[route][nextStop]['lng']
    finalLatitude = abs(latitude - stopLatitude)
    finalLongitude = abs(longitude - stopLongitude)
    return [((finalLatitude**2) + (finalLongitude**2))**(1/2)]