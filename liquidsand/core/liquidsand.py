#!/usr/bin/python

import sys
sys.path.append("liquidsand/base/")

from widget import widget
from config import config_var, config_file_reader

from gui import gui
from apps import apps

class liquidsand(widget):
    def __init__(self, name):
        widget.__init__(self, name)

        # debug
        self.debug = config_var("debug", True)
        self.debug.hook = self.update_debug
        #enable / disable debug
        self.debug.set(True)

        #config path
        config_file_reader.config_path = "conf"

        cfr = config_file_reader()
        cfr.debug()

        self.gui = gui("gui")
        self.apps = apps("apps")
        self.log_debug("init liquidsand done")

    def update_debug(self):
        widget.debug = self.debug.get()
