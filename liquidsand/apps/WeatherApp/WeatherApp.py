#!/usr/bin/env python3

import pyowm

from app import app
from config import config_var, config_file_reader, config_utils as cu

class WeatherApp(app):

    __instance = None

    @staticmethod
    def get_instance():
        if WeatherApp.__instance == None:
            WeatherApp.__instance = WeatherApp()
        return WeatherApp.__instance

    def __init__(self, name="WeatherApp"):
        app.__init__(self, name)

        # weather api url
        self.api_url = config_var("api_url", "http://api.openweathermap.org")
        self.api_weather = config_var("api_weather", "/data/2.5/weather")

        # user configuration
        self.city_list = config_var("city_list", ["Aachen,de", "Wuerzburg,de", "Bonn,de"])
        self.cur_city = config_var("cur_city", "Aachen,de")
        self.user_key = config_var("user_key", "key")
        self.update_freq = config_var("upate_freq", "10m")
        self.temp_unit = config_var("temp_unit", "celsius")
        self.update_freq.hook = self.update_freq_hook

        cfr = config_file_reader()
        cfr.debug()

        self.owm = pyowm.OWM(self.user_key.get())

        # init updates
        self.register_update(self.update, cu.to_sec(self.update_freq.get()))

        self.update()
        self.log_debug("init weather done")

    def update(self):
        self.observation = self.__do_request(self.owm.weather_at_place)
        self.forecast = self.__do_request(self.owm.daily_forecast)
        if self.observation == None or self.forecast == None:
            return
        self.weather = self.observation.get_weather()
        self.log_debug(str(self.weather))
        self.log_debug(str(self.forecast))
        self.log_debug("current temperature: "
                + str(self.weather.get_temperature(self.temp_unit.get())["temp"])
                + " " + self.temp_unit.get())
        self.log_debug("will be sunny in " + self.cur_city.get() + " tomorrow? "
                + str(self.forecast.will_be_sunny_at(pyowm.timeutils.tomorrow())))

    def update_freq_hook(self):
        self.register_update(self.update, cu.to_sec(self.update_freq.get()))

    def __do_request(self, request):
        req = None
        try:
            req = request(self.cur_city.get())
        except pyowm.exceptions.api_call_error.APICallError:
            self.log_error("invalid API Key (UNAUTHORIZED)")
        return req
