#!/usr/bin/env python3
import requests, os
import datetime
from pprint import pprint
from sys import argv

ASTRONOMYAPI_ID=os.getenv("ASTRONOMYAPI_ID")
ASTRONOMYAPI_SECRET=os.getenv("ASTRONOMYAPI_SECRET")
ERROR_MSG = "Error"

if len(argv) > 1:
    # assume that argv[1] is ip address, ip address is not checked for validity or format
    ip_addr = argv[1]
else:
    ip_addr = '165.225.57.244' # default to this ip address

def get_location(ip_addr):
    """Returns the longitude and latitude for the location of this machine.
    Returns:
    str: latitude
    str: longitude"""
    url = 'http://ip-api.com/json/{ip}'.format(ip=ip_addr)
    response = requests.get(url)
    data = response.json()
#    print (data)
    if data['status'] == 'success':
        return data['lat'], data['lon']
    else:
        return ERROR_MSG, ERROR_MSG

def get_sun_position(latitude, longitude):
    """Returns the current position of the sun in the sky at the specified location
    Parameters:
    latitude (str)
    longitude (str)
    Returns:
    float: azimuth
    float: altitude
    """
    let_elevation = "200" # assume elevation of the location as 200 meters; need a funciton to find elevation based on lat and lon
    curr_dt = datetime.date.today().isoformat()
    curr_time = datetime.datetime.now().strftime("%H:%M:%S")
    params_dict = {"latitude":latitude, "longitude":longitude, "elevation":let_elevation, "from_date":curr_dt, "to_date":curr_dt, "time":curr_time}
#    response_2 = requests.get('https://api.astronomyapi.com/api/v2/bodies', auth=(ASTRONOMYAPI_ID, ASTRONOMYAPI_SECRET))
    response_2 = requests.get('https://api.astronomyapi.com/api/v2/bodies/positions/sun', auth=(ASTRONOMYAPI_ID, ASTRONOMYAPI_SECRET), params = params_dict)
    if response_2.status_code == 200:
        data_2 = response_2.json()['data']['table']['rows'][0]['cells'][0]['position']['horizontal']
        return data_2['azimuth']['degrees'], data_2['altitude']['degrees']
    else:
        return ERROR_MSG, ERROR_MSG

def print_position(azimuth, altitude):
    """Prints the position of the sun in the sky using the supplied coordinates
    Parameters:
    azimuth (float)
    altitude (float)"""
    print("The Sun is currently at:", azimuth, "degrees azimuth,", altitude, "degrees altitude")

if __name__ == "__main__":
    latitude, longitude = get_location(ip_addr)
    if latitude == ERROR_MSG and longitude == ERROR_MSG:
        print ("Error finding latitude and longitude")
        exit ()
    
    azimuth, altitude = get_sun_position(latitude, longitude)
    if azimuth == ERROR_MSG and altitude == ERROR_MSG:
        print ("Error finding azimuth and altitude")
        exit ()
    
    print_position(azimuth, altitude)
