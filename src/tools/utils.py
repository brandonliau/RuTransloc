# Standard library imports
import sys, os
sys.path.append(os.path.abspath('../../configuration'))
# Third party imports
import requests
# Local imports
import config as con

def vehicleAPI(route: str) -> dict:
	"""
    :param: route
    :return: Data for each vehicle on the given route
    :usage: Provides raw vehicle data
	"""
	url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"
	querystring = {"agencies":f"{con.agencyID}", "routes":f"{route}", "callback":"call"}
	headers = {
		"X-RapidAPI-Key": con.rapidApiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return(response.json())

def weatherAPI(latitude: float, longitude: float) -> dict:
	"""
    :param: latitude, longitude
    :return: Weather at given coordinates
    :usage: Provides raw weather
	"""
	response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,precipitation,visibility,windspeed_10m&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&forecast_days=1")
	# print(f'weather_status: {response.status_code}, {time.strftime("%b %d %H:%M:%S", time.localtime())}') # Used for debugging purposes
	return(response.json())

def trafficAPI(latitude: float, longitude: float) -> dict:
	"""
    :param: latitude, longitude
    :return: Traffic at given coordinates
    :usage: Provides raw traffic data
	"""
	trafficApiKey = next(con.trafficApiKeys)
	while True:
		response = requests.get(f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={trafficApiKey}&point={latitude},{longitude}")
		if response.status_code == 200:
			# print(f'traffic_status: {response.status_code}, {time.strftime("%b %d %H:%M:%S", time.localtime())}') # Used for debugging purposes
			return(response.json())
		else:
			trafficApiKey = next(con.trafficApiKeys)

def agencyAPI():
	url = "https://transloc-api-1-2.p.rapidapi.com/agencies.json"
	headers = {
		"X-RapidAPI-Key": con.rapidApiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers)
	return(response.json())

def routesAPI():
	url = "https://transloc-api-1-2.p.rapidapi.com/routes.json"
	querystring = {"agencies":"1323","callback":"call"}
	headers = {
		"X-RapidAPI-Key": con.rapidApiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	return(response.json())

def stopsAPI(agencyID: str) -> dict:
	"""
    :param: agencyID
    :return: All stops for the given agency
    :usage: Provides raw stop data
	"""
	url = "https://transloc-api-1-2.p.rapidapi.com/stops.json"
	querystring = {"agencies":f"{agencyID}", "callback":"call"}
	headers = {
		"X-RapidAPI-Key": con.rapidApiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return(response.json())

print(routesAPI())