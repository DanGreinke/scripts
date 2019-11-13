#! /bin/bash/python3

import json
import requests
import sys
import pprint

current_weather = requests.get('https://samples.openweathermap.org/data/2.5/weather?q=M%C3%BCnchen,DE&appid=b6907d289e10d714a6e88b30761fae22')
weather_data = json.loads(current_weather.text)
#pprint.pprint(current_weather.text)

print(weather_data['weather'][0]['main'] + ' - ' + weather_data['weather'][0]['description'])
