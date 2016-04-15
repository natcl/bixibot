#!/usr/local/bin/python2.7
# encoding: utf-8

import web
import requests
import re
from urllib2 import urlopen
import xml.etree.cElementTree as ET
import json
import random
import os

STATION = 'Guizot / Saint-Laurent'
numStations = 15

urls = (
    "/", "index",
    "/station", "station"
)

app = web.application(urls, globals())

class index:
    def GET(self):
        if get_station_info(STATION):
            bikes, stations = get_station_info(STATION)
            return 'Velos: {0} Stations: {1}'.format(bikes, stations)
        else:
            return 'No data'

class station:
    def GET(self):
        web.header('Content-Type', 'application/json')
        state = ''
        data = update_station()
        for c in json.loads(data):
            state += str(c)
        #update_spark(state)
        return data

def init_station():
    if not os.path.exists('bixi.json'):
        tableau = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
        index_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        station_info = get_station_info(STATION)
        if station_info:
            bikes, stations = station_info
        else:
            bikes, stations = (0, 0)
        lockedStations = numStations - (bikes + stations)

        for x in range(bikes):
            index = random.choice(index_list)
            index_list.remove(index)
            tableau[index] = 1

        for x in range(stations):
            index = random.choice(index_list)
            index_list.remove(index)
            tableau[index] = 0

        for x in range(lockedStations):
            index = random.choice(index_list)
            index_list.remove(index)
            tableau[index] = 2

        with open('bixi.json', 'w') as f:
            f.write(json.dumps(tableau))
        return json.dumps(tableau)

def update_station():
    if os.path.exists('bixi.json'):
        with open('bixi.json', 'r') as f:
            previous_state = json.loads(f.read())

        stations_index = []
        bikes_index = []
        locked_index = []

        for (i, v) in enumerate(previous_state):
            if v == 0:
                stations_index.append(i)
            if v == 1:
                bikes_index.append(i)
            if v == 2:
                locked_index.append(i)


        station_info = get_station_info(STATION)
        if station_info:
            bikes, stations = station_info
        else:
            bikes, stations = (0, 0)
        lockedStations = numStations - (bikes + stations)

        previous_bikes = len(bikes_index)
        previous_stations = len(stations_index)
        previous_locked = len(locked_index)

        if previous_stations == stations and previous_bikes == bikes and previous_locked == lockedStations:
            return json.dumps(previous_state)

        if lockedStations > previous_locked:
            locked_diff = lockedStations - previous_locked
            for x in range(locked_diff):
                try:
                    i = random.choice(stations_index)
                    previous_state[i] = 2
                    stations_index.remove(i)
                except IndexError:
                    break

        if lockedStations < previous_locked:
            locked_diff = previous_locked - lockedStations
            for x in range(locked_diff):
                try:
                    i = random.choice(locked_index)
                    previous_state[i] = 0
                    locked_index.remove(i)
                except IndexError:
                    break

        if bikes > previous_bikes:
            bike_diff = bikes -  previous_bikes
            for x in range(bike_diff):
                try:
                    i = random.choice(stations_index)
                    previous_state[i] = 1
                    stations_index.remove(i)
                except IndexError:
                    break

        if stations > previous_stations:
            station_diff = stations - previous_stations
            for x in range(station_diff):
                try:
                    i = random.choice(bikes_index)
                    previous_state[i] = 0
                    bikes_index.remove(i)
                except IndexError:
                    break

        with open('bixi.json', 'w') as f:
            f.write(json.dumps(previous_state))
        return json.dumps(previous_state)

    else:
        init_station()


def get_station_info(query):
    streetNames = query.lower().replace(' ', '').split('/')
    found = False

    for URL in ["http://montreal.bixi.com/data/bikeStations.xml"]:
        feed = urlopen(URL)
        tree = ET.parse(feed)
        for station in tree.getroot().findall("station"):
            nbBikes = station.find("nbBikes").text
            nbEmptyDocks = station.find("nbEmptyDocks").text
            station_name = station.find("name").text
            station_lat = re.sub(r"\s", "", station.find("lat").text)
            station_long = re.sub(r"\s", "", station.find("long").text.strip())
            station_installed = station.find("installed").text
            station_locked = station.find("locked").text
            if (station_installed == "true" and station_locked != "true"):
                parsed_station_name = station_name.lower().replace(' ', '').split('/')
                # if only one argument is given
                if len(streetNames) == 1:
                    if streetNames[0] in parsed_station_name:
                        found = True
                        result = (nbBikes, nbEmptyDocks)
                # if 2 arguments are given
                if len(streetNames) == 2:
                    if (streetNames[0] in parsed_station_name and streetNames[1] in parsed_station_name):
                        found = True
                        result = (int(nbBikes), int(nbEmptyDocks))
        if (found):
            return result
        else:
            return False

if __name__ == "__main__":
    app.run()
