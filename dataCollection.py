import getData as gd
import config as con
import time as tm
import csv
import os

for route in con.routeLst:
    if os.path.isfile(f'{route}') == False:
        with open(f'{route}.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
    if os.stat(f'{route}.csv').st_size == 0:
        header = ['Time', 'Speed', 'Vehicle_id', 'Passenger_load', 'Next_stop, ''Latitude', 'Longitude', 'Heading', 'Temperature', 'Windspeed', 'Precipitation', 'Humidity', 'Visibility']
        with open(f'{route}.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(header)

starttime = tm.time()
while True:
    for route in con.routeLst:
        vehicleData = gd.getVehicleData(route)
        nextStop = vehicleData[4]
        latitude = vehicleData[5]
        longitude = vehicleData[6]
        weatherData = gd.getWeatherData(latitude, longitude)
        distanceData = gd.getDistance(route, nextStop, latitude, longitude)
        rowData = vehicleData + weatherData + distanceData
        with open(f'{route}.csv', 'a', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(rowData)
    tm.sleep(10.0 - ((tm.time() - starttime) % 10.0))