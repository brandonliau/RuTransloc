import dataManagement as dm
from sklearn import svm
import threading
import csv
import os

dataFile = 'data.csv'
def collection():
    threading.Timer(10.0, collection).start()
    response = dm.requestData(4012650)
    data = response['data']['1323']
    for bus in data:
        busData = []
        time = bus['last_updated_on']
        speed = bus['speed']
        vehicle_id = bus['vehicle_id']
        passenger_load = bus['passenger_load']
        tracking_status = bus['tracking_status']
        latitude = bus['location']['lat']
        longitude = bus['location']['lng']
        heading = bus['heading']
        busData = [time, speed, vehicle_id, passenger_load, tracking_status, latitude, longitude, heading]
        with open(dataFile, 'a', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(busData)

if os.stat(dataFile).st_size == 0:
    header = ['Time', 'Speed', 'Vehicle_id', 'Passenger_load', 'Tracking_status', 'Latitude', 'Longitude', 'Heading']
    with open('./data.csv', 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(header)

collection()