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

def get_current_weather():
    last_update = []
    last_update_time = time.ctime(current_weather_data['dt'])
    current_temp = current_weather_data['main']['temp'] - 273.15
    temp_str = ("%.2f" %current_temp) + " C"
    weather_now = current_weather_data['weather'][0]['main']
    last_update = [last_update_time, temp_str, weather_now]
    return last_update

def get_forecast_time(sample):
    sample_epoch = forecast_data['list'][sample]['dt']
    sample_time = time.ctime(sample_epoch)
    return sample_time

def get_forecast_temp(sample):
    sample_temp = forecast_data['list'][sample]['main']['temp'] - 273.15
    sample_temp_str = ("%.2f" %sample_temp) + " C"
    return sample_temp_str

def get_forecast_weather(sample):
    sample_weather = forecast_data['list'][sample]['weather'][0]['main']
    return sample_weather

def main():
    print("Location: " + forecast_data['city']['name'])
    print(get_current_weather()[0] + " .... " + "Temp: " + get_current_weather()[1] + " .... " + get_current_weather()[2])

    for bin in range(0,9):
        print(get_forecast_time(bin) + " .... " + "Temp: " + get_forecast_temp(bin) + " .... " + get_forecast_weather(bin))

main()
