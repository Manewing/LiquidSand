#!/usr/bin/python

import sys
sys.path.append("liquidsand/apps/")

from widget import widget
from config import config_var, config_file_reader

class apps(widget):
    def __init__(self, name):
        widget.__init__(self, name)

        # list of apps
        self.app_list = config_var("app_list",  ["WeatherApp"])
        cfr = config_file_reader()
        cfr.debug()

        self.app_list.set(["WeatherApp"])

        # load apps
        self.__initialize()

        self.log_debug("init apps done")

    def __initialize(self):
        for app in self.app_list.get():
            self.log_debug("checking for: liquidsand/apps/" + app)
            sys.path.append("liquidsand/apps/"+app+"/")
            try:
                app_module = __import__(app, fromlist=app)
                app_widget = getattr(app_module, app)
                setattr(self, app, app_widget.get_instance())
            except ImportError as e:
                self.log_error("could not load app: " + app)
                self.log_error("ImportError: " + str(e))


