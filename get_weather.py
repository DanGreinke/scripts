#! /bin/bash/python3

import datetime, time
import json
import requests
import yaml

credentials = yaml.safe_load(open('secrets.yaml'))
api_key = credentials['WEATHER_API']

current_weather = requests.get('https://api.openweathermap.org/data/2.5/weather?q=San+Francisco,us&appid={}'.format(api_key))
current_weather_data = json.loads(current_weather.text)

forecast_weather = requests.get('https://api.openweathermap.org/data/2.5/forecast?q=San+Francisco,us&appid={}'.format(api_key))
forecast_data = json.loads(forecast_weather.text)


def get_time(sample, forecast):
    if forecast == True:
        sample_epoch = forecast_data['list'][sample]['dt']
    else:
        sample_epoch = current_weather_data['dt']

    sample_time = time.ctime(sample_epoch)
    return sample_time

def get_temp(sample, forecast):
    if forecast == True:
        sample_temp = forecast_data['list'][sample]['main']['temp'] - 273.15
    else:
        sample_temp = current_weather_data['main']['temp'] - 273.15
    sample_temp_str = ("%.2f" %sample_temp) + " C"
    return sample_temp_str

def get_weather(sample, forecast):
    if forecast == True:
        sample_weather = forecast_data['list'][sample]['weather'][0]['main']
    else:
        sample_weather = current_weather_data['weather'][0]['main']
    sample_weather = forecast_data['list'][sample]['weather'][0]['main']
    return sample_weather

def main():
    print("Location: " + forecast_data['city']['name'])
    print(get_time(-1,False) + " .... " + "Temp: " + get_temp(-1, False) + " .... " + get_weather(-1, False))

    for bin in range(0,9):
        print(get_time(bin, True) + " .... " + "Temp: " + get_temp(bin, True) + " .... " + get_weather(bin, True))

main()
