import requests
from config import apiKey

def requestData(busID):
	url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"

	querystring = {"agencies":"1323","routes":f"{busID}","callback":"call"}

	headers = {
		"X-RapidAPI-Key": apiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	return(response.json())

# class Vehicle:
# 	def __init__(self, time: datetime, speed: float, vehicle_id: int, passenger_load: float, tracking_status: str, latitude: float, longitude: float, heading: int) -> None:
# 		self.time = time
# 		self.speed = speed
# 		self.vehicle_id = vehicle_id
# 		self.passenger_load = passenger_load
# 		self.tracking_status = tracking_status
# 		self.latitude = latitude
# 		self.longitude = longitude
# 		self.heading = heading


 # busData = dm.Vehicle(time, speed, vehicle_id, passenger_load, tracking_status, latitude, longitude, heading)
    # time = bus['last_updated_on']
    # speed = bus['speed']
    # vehicle_id = bus['vehicle_id']
    # passenger_load = bus['passenger_load']
    # tracking_status = bus['tracking_status']
    # latitude = bus['location']['lat']
    # longitude = bus['location']['lng']
    # heading = bus['heading']
    # busData = dm.Vehicle(time, speed, vehicle_id, passenger_load, tracking_status, latitude, longitude, heading)


 # busData = {}
    # busData['time'] = bus['last_updated_on']
    # busData['speed'] = bus['speed']
    # busData['vehicle_id'] = bus['vehicle_id']
    # busData['passenger_load'] = bus['passenger_load']
    # busData['tracking_status'] = bus['tracking_status']
    # busData['latitude'] = bus['location']['lat']
    # busData['longitude'] = bus['location']['lng']
    # busData['heading'] = bus['heading']