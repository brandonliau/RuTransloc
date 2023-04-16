import routeInfo as ri
import getData as gd
import time as tm
import csv
import os

for route in ri.routeLst:
    if os.path.isfile(f'{route}.csv') == False:
        with open(f'{route}.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
    if os.stat(f'{route}.csv').st_size == 0:
        header = ['Time', 'Vehicle_id', 'Speed', 'Passenger_load', 'Next_stop', 'Latitude', 'Longitude', 'Heading', 'Traffic_speed', 'Temperature', 'Windspeed', 'Precipitation', 'Humidity', 'Visibility', 'Stop_distance']
        with open(f'{route}.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(header)

while True:
    starttime = tm.time()
    for route in ri.routeLst:
        vehicleLst = gd.getVehicleData(route)
        for vehicleData in vehicleLst:
            nextStop = vehicleData[4]
            latitude = vehicleData[5]
            longitude = vehicleData[6]
            trafficData = gd.getTrafficData(latitude, longitude)
            weatherData = gd.getWeatherData(latitude, longitude)
            distanceData = gd.getDistance(route, nextStop, latitude, longitude)
            rowData = vehicleData + trafficData + weatherData + distanceData
            with open(f'{route}.csv', 'a', encoding='UTF8') as file:
                writer = csv.writer(file)
                writer.writerow(rowData)
    if os.path.isfile('stop'):
        break
    if 10.0 - (tm.time() - starttime) >= 0:
        tm.sleep(10.0 - (tm.time() - starttime))