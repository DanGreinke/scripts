#! /bin/bash/python3

import datetime, time
import json
import requests
import sys
import yaml

credentials = yaml.safe_load(open('secrets.yaml'))
api_key = credentials['WEATHER_API']

#current_weather = requests.get('https://samples.openweathermap.org/data/2.5/weather?q=M%C3%BCnchen,DE&appid=b6907d289e10d714a6e88b30761fae22')
#weather_data = json.loads(current_weather.text)
#pprint.pprint(current_weather.text)

forecast_weather = requests.get('https://api.openweathermap.org/data/2.5/forecast?q=San+Francisco,us&appid={}'.format(api_key))
forecast_data = json.loads(forecast_weather.text)
#pprint.pprint(forecast_data)

def get_time(sample):
    sample_epoch = forecast_data['list'][sample]['dt']
    sample_time = time.ctime(sample_epoch)
    return sample_time

def get_temp(sample):
    sample_temp = forecast_data['list'][sample]['main']['temp'] - 273.15
    sample_temp_str = ("%.2f" %sample_temp) + " C"
    return sample_temp_str

def get_weather(sample):
    sample_weather = forecast_data['list'][sample]['weather'][0]['main']
    return sample_weather

def main():
    print("Location: " + forecast_data['city']['name'])
    for bin in range(0,9):
        print(get_time(bin) + " .... " + "Temp: " + get_temp(bin) + " .... " + get_weather(bin))

main()
