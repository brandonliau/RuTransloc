import config as con
import requests
import time

def vehicleAPI(route: str) -> dict:
	"""
    :param: route
    :return: Data for each vehicle on the given route
    :usage: Provides raw vehicle data
	"""
	url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"
	querystring = {"agencies":f"{con.agencyID}", "routes":f"{route}", "callback":"call"}
	headers = {
		"X-RapidAPI-Key": con.apiKey,
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
	print(f'status_code: {response.status_code}, {time.strftime("%H:%M:%S", time.localtime())}') # Used for debugging purposes
	return(response.json())

def trafficAPI(latitude: float, longitude: float) -> dict:
	"""
    :param: latitude, longitude
    :return: Traffic at given coordinates
    :usage: Provides raw traffic data
	"""
	trafficAPIKey = next(con.trafficAPIKeys)
	while True:
		print(trafficAPIKey)
		response = requests.get(f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={trafficAPIKey}&point={latitude},{longitude}")
		if response.status_code == 200:
			return(response.json())
		else:
			trafficAPIKey = next(con.trafficAPIKeys)

def stopsAPI(agencyID: str) -> dict:
	"""
    :param: agencyID
    :return: All stops for the given agency
    :usage: Provides raw stop data
	"""
	url = "https://transloc-api-1-2.p.rapidapi.com/stops.json"
	querystring = {"agencies":f"{agencyID}", "callback":"call"}
	headers = {
		"X-RapidAPI-Key": con.apiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return(response.json())
