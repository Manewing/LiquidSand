#!/usr/bin/python

from widget import widget

import json
import atexit

#@class configuration variable
#@brief variable which is set through configuration file
class config_var(widget):

    #@brief constructor
    #@param name  - name of variable
    #@param value - value to set (initial/default)
    def __init__(self, name, value):
        widget.__init__(self, name)
        self.__value = value
        self.__hook = None

    #@brief get value
    #@return value of variable
    def get(self):
        return self.value

    #@brief set value (triggers hook)
    #@param value - value to set
    def set(self, value):
        self.value = value


    #@brief get value
    #@return value of variable
    @property
    def value(self):
        return self.__value

    #@brief set value (triggers hook)
    #@param value - value to set
    @value.setter
    def value(self, value):
        if self.__hook != None:
            self.__hook()
        self.__value = value

    #@brief get hook
    #@return hook which is called on variable change
    @property
    def hook(self):
        return self.__hook

    #brief set hook
    #@param hook - hook function to set
    @hook.setter
    def hook(self, hook):
        self.__hook = hook

# @class configuration file reader
# @brief reads in configuration file (JSON) and sets all
#        configuration variables of its parent class,
#        if the configuration file does not exist a new one is created
#        by writing the default values of the configuration varibles to the file
class config_file_reader(widget):

    #@brief constructor, reads in file
    #@param filename - name of the configuration file
    def __init__(self, filename):
        widget.__init__(self, "config_file_reader")
        self.__filename = filename
        self.__changed = False
        self.__read_file()
        atexit.register(self.exit)

    #@brief called at exit, writes changes to file
    def exit(self):
        if self.__changed == True:
            self.__write_file()

    #@brief hook for config_var changes
    def hook(self):
        self.__changed = True

    #@brief set config var by name
    #@param name  - (non hierachical) name of config var
    #@param value - value to set
    def __set_config_var(self, name, value):
        name = widget.get_base_name(self.name) + "." + name
        obj = widget.get(name)
        if obj == None:
            return
        if isinstance(obj, config_var):
            obj.value = value

    #@brief get config var by name
    #@aram name  - (non hierachical) name of config var
    #@return reference of config var or None
    def __get_config_var(self, name):
        name = widget.get_base_name(self.name) + "." + name
        return widget.get(name)

    #@brief add hooks to all config vars
    def __add_hooks(self):
        obj = self.get_parent()
        config_vars = obj.find_subinstances(None,
                lambda x: ( isinstance(x, config_var) ))
        for cvar in config_vars.itervalues():
            cvar.hook = self.hook

    #@brief reads in file or creates new one if file does not exist
    def __read_file(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            for key, value in data.iteritems():
                self.__set_config_var(key, value)
        except IOError as e:
            self.log_warning("could not open " + self.filename + ", creating new")
            self.__write_file()
        self.__add_hooks()

    #@brief write values of config vars to file
    def __write_file(self):
        obj = self.get_parent()
        config_vars = obj.find_subinstances(None,
                lambda x: ( isinstance(x, config_var) ))
        new_data = dict()
        for key, obj in config_vars.iteritems():
            key = (lambda x: x if x.rfind(".") == -1 else x[x.rfind(".")+1:])(key)
            new_data[key] = obj.value
        with open(self.filename, "w") as f:
            json.dump(new_data, f)

    #@brief get filename
    #@return filename
    @property
    def filename(self):
        return self.__filename


