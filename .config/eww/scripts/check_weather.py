#!/usr/bin/env python3.10
import requests
import json
from pathlib import Path, PosixPath
from sys import argv

class Weather:
    def __init__(self, api_key: str, latitude: float, longitude: float, cache_dir: str):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.cache_dir = Path.expanduser(PosixPath(cache_dir))

        Path.mkdir(self.cache_dir, parents=True, exist_ok=True)
        if Path.exists((weather_json := self.cache_dir / 'weather.json')):
            with open(weather_json, 'r') as in_file:
                self.data = json.load(in_file)
        else:
            self.data = {}
    
    def fetch(self):
        r = requests.get(
            url="https://api.openweathermap.org/data/2.5/onecall",
            params={
                'lon': self.longitude,
                'lat': self.latitude,
                'units': 'imperial',
                'appid': self.api_key,
                'exclude': 'minutely,hourly,daily'
            }
        )
        if r.status_code == 200:
            self.data = r.json()
            self.dump()
        
    
    def dump(self):
        self.cache('weather-temp', self.temperature)
        self.cache('weather-conditions', self.conditions)
        with open(self.cache_dir / 'weather.json', 'w') as out_file:
            json.dump(self.data, out_file)
    
    def cache(self, file_name: str, data):
        with open(self.cache_dir / file_name, 'w') as cache_file:
            if type(data) is tuple:
                cache_file.write('\n'.join(data))
            else:
                cache_file.write(str(data))

    @property
    def temperature(self) -> int:
        try:
            return int(self.data['current']['temp'])
        except KeyError:
            return 0
    
    @property
    def conditions(self) -> tuple[str, str]:
        icons = {
            '01d': '',
            '01n': '',
            '02d': '',
            '02n': '',
            '03d': '',
            '03n': '',
            '04d': '',
            '04n': '',
            '09d': '',
            '09n': '',
            '10d': '',
            '10n': '',
            '11d': '',
            '11n': '',
            '13d': '',
            '13n': '',
            '50d': '',
            '50n': ''
        }
        try:
            return (
                self.data['current']['weather'][0]['description'].capitalize(),
                icons.get(self.data['current']['weather'][0]['icon'])
            )
        except KeyError:
            return ('', '')
    
    @property
    def alerts(self) -> str:
        alerts = []
        if 'alerts' not in self.data:
            return alerts
        else:
            for alert in self.data['alerts']:
                alerts.append(f" {alert['event']}")
            return alerts


if __name__ == "__main__":
    w = Weather(
        api_key='3bdcaceaa4992d1e2c2fd3b1b0e8bb24',
        latitude=30.4383,
        longitude=-84.2807,
        cache_dir="~/.cache/eww"
    )
    if argv[1] == 'fetch':
        w.fetch()
    elif argv[1] == 'temperature':
        print(w.temperature)
    elif argv[1] == 'conditions':
        if len(argv) > 2:
            if argv[2] == 'description':
                print(w.conditions[0])
            elif argv[2] == 'icon':
                print(w.conditions[1])
        else:
            for line in w.conditions:
                print(line)
    elif argv[1] == 'rain':
        print(w.rain_forecast)
    elif argv[1] == 'alerts':
        for alert in w.alerts:
            print(alert)