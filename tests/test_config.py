#!/bin/usr/python

import sys
sys.path.append("../liquidsand/base/")

from widget import widget
from config import config_var, config_file_reader

class test(widget):
    def __init__(self, name):
        widget.__init__(self, name)
        self.url = config_var("url", "www.yahoo.de")
        self.key = config_var("key", "asdf")
        self.log_debug("initial values:")
        self.url.log_debug("-> .value = " + self.url.value)
        self.key.log_debug("-> .value = " + self.key.value)
        cfr = config_file_reader()
        cfr.debug()
        self.log_debug("init test done")

class system(widget):
    def __init__(self, name):
        widget.__init__(self, name)

        # init config variables

        #debug
        self.debug = config_var("debug", False)
        self.debug.hook = self.update_debug
        # enable debug
        self.debug.set(True)

        # config path
        self.config_path = config_var("config_path", "conf")
        self.config_path.hook = self.update_config_path

        # test variable list
        self.var_list = config_var("var_list", ["item"])

        self.log_debug("initial values:")
        self.log_debug("-> .debug = True")
        self.log_debug("-> .config_path = " + self.config_path.get())
        self.log_debug("-> .var_list = " + str(self.var_list.value))

        cfr = config_file_reader()
        cfr.debug()

        # init test class
        self.t = test("test")
        self.log_debug("init system done")

    def update_debug(self):
        widget.debug = self.debug.get()

    def update_config_path(self):
        config_file_reader.config_path = self.config_path.get()

if __name__ == "__main__":
    sys = system("system")
    print "Enter new url:"
    sys.t.url.value = raw_input()
    print "Enter new key:"
    sys.t.key.value = raw_input()
