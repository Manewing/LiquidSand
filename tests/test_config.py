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
        print "initial values:"
        self.url.log("my value = " + self.url.value)
        self.key.log("my value = " + self.key.value)
        file_reader = config_file_reader("test.json")
        print "after reading of config file"
        self.url.log("my value = " + self.url.value)
        self.key.log("my value = " + self.key.value)

class system(widget):
    def __init__(self, name):
        widget.__init__(self, name)
        self.t = test("test")

if __name__ == "__main__":
    sys = system("system")
    print "Enter new url:"
    sys.t.url.value = raw_input()
    print "Enter new key:"
    sys.t.key.value = raw_input()
