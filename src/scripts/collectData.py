# Standard library imports
import sys, os, traceback
import time as tm
sys.path.append(os.path.abspath('../../configuration'))
sys.path.append(os.path.abspath('../tools'))
# Third party imports
import requests, json, csv
# Local imports
import config as con
import routeInfo as ri
import getData as gd

for route in con.chooseRoutes:
    if os.path.isfile(f'{route}.csv') == False:
        with open(f'{route}.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
    if os.stat(f'{route}.csv').st_size == 0:
        header = ['Time', 'Call_name', 'Speed', 'Passenger_load', 'Next_stop', 'Latitude', 'Longitude', 'Heading', 'Traffic_speed', 'Temperature', 'Windspeed', 'Precipitation', 'Humidity', 'Visibility', 'Stop_distance']
        with open(f'{route}.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(header)

while True:
    try:
        starttime = tm.time()
        for route in ri.chosenRoutes:
            vehicles = gd.getVehicleData(route)
            for vehicleData in vehicles:
                nextStop = vehicleData[4]
                latitude = vehicleData[5]
                longitude = vehicleData[6]
                trafficData = gd.getTrafficData(latitude, longitude)
                weatherData = gd.getWeatherData(latitude, longitude)
                distanceData = gd.getDistance(route, nextStop, latitude, longitude)
                rowData = vehicleData + trafficData + weatherData + distanceData
                with open(f'{ri.allRoutes[route]}.csv', 'a', encoding='UTF8') as file:
                    writer = csv.writer(file)
                    writer.writerow(rowData)
        if os.path.isfile('stop'):
            break
        if 10.0 - (tm.time() - starttime) >= 0:
            tm.sleep(10.0 - (tm.time() - starttime))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        traceback.print_exc()
        if 5.0 - (tm.time() - starttime) >= 0:
            tm.sleep(5.0 - (tm.time() - starttime))
        continue
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error decoding JSON: {e}")
        traceback.print_exc()
        if 5.0 - (tm.time() - starttime) >= 0:
            tm.sleep(10.0 - (tm.time() - starttime))
        continue
    except Exception as e:
        print(f"Unknown error: {e}")
        traceback.print_exc()
        if 5.0 - (tm.time() - starttime) >= 0:
            tm.sleep(10.0 - (tm.time() - starttime))
        continue