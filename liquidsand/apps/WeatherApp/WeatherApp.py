#!/usr/bin/env python3

import sys
sys.path.append("liquidsand/base")

from widget import widget
from config import config_var, config_file_reader

class WeatherApp(widget):

    __instance = None

    @staticmethod
    def get_instance():
        if WeatherApp.__instance == None:
            WeatherApp.__instance = WeatherApp()
        return WeatherApp.__instance

    def __init__(self, name="WeatherApp"):
        widget.__init__(self, name)

        # weather api url
        self.api_url = config_var("api_url", "http://api.openweathermap.org")
        self.api_weather = config_var("api_weather", "/data/2.5/weather")

        # user configuration
        self.city_list = config_var("city_list", ["Aachen", "Wuerzburg", "Bonn"])
        self.cur_city = config_var("cur_city", "Aachen")
        self.user_key = config_var("user_key", "key")

        cfr = config_file_reader()
        cfr.debug()
        self.log_debug("init weather done")



