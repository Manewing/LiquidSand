#!/usr/bin/python

import inspect

class meta_widget(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.finalize()
        return obj

class widget(object):
    __instances = dict()
    __base_level = ""

    __metaclass__ = meta_widget

    def __init__(self, name):
        name = name.replace(".", "");
        self.__name = widget.__get_name(name)
        self.__add_instance()
        widget.__add_base_level(name)

    def finalize(self):
        widget.__remove_base_level()

    @staticmethod
    def __get_name(name):
        if widget.__base_level == "":
            return name
        return widget.__base_level + "." + name

    @staticmethod
    def __add_base_level(level):
        if widget.__base_level == "":
            widget.__base_level = level
            return
        widget.__base_level = widget.__base_level + "." + level

    @staticmethod
    def __remove_base_level():
        if widget.__base_level == "":
            return
        index = widget.__base_level.rfind(".")
        widget.__base_level = widget.__base_level[:index]

    def __add_instance(self):
        if widget.__instances.get(self.name) != None:
            self.log_error("<- instance(name) already exits")
            # TODO generate random string?
            return
        widget.__instances[self.name] = self

    def log(self, log, prefix=""):
        #TODO add log file
        print(prefix + self.name + ": " + log)

    def log_warning(self, warning):
        self.log(warning, "WARNING: ")

    def log_error(self, error):
        self.log(error, "ERROR: ")

    @property
    def name(self):
        return self.__name

    def get(name):
        return widget.__instances[name]
