import config as con
import requests

def vehicleAPI(route):
	url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"
	querystring = {"agencies":f"{con.agencyID}", "routes":f"{route}", "callback":"call"}
	headers = {
		"X-RapidAPI-Key": con.apiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return(response.json())

def stopsAPI():
	url = "https://transloc-api-1-2.p.rapidapi.com/stops.json"
	querystring = {"agencies":f"{con.agencyID}", "callback":"call"}
	headers = {
		"X-RapidAPI-Key": con.apiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return(response.json())

def routesAPI():
	url = "https://transloc-api-1-2.p.rapidapi.com/routes.json"
	querystring = {"agencies":f"{con.agencyID}", "callback":"call"}
	headers = {
		"X-RapidAPI-Key": con.apiKey,
		"X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return(response.json())

def weatherAPI(latitude, longitude):
	response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,precipitation,visibility,windspeed_10m&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&forecast_days=1")
	return(response.json())

def trafficAPI(latitude, longitude):
	response = requests.get(f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={con.trafficAPIKey1}&point={latitude},{longitude}")
	return(response.json())