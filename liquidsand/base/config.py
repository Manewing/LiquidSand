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
        self.__hooks = list()

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
        self.__value = value
        for hook in self.__hooks:
            hook()

    #@brief add hooks
    #@return hook which is called on variable change
    @property
    def hook(self):
        return self.__hooks

    #brief set hook
    #@param hook - hook function to set
    @hook.setter
    def hook(self, hook):
        self.__hooks.append(hook)

# @class configuration file reader
# @brief reads in configuration file (JSON) and sets all
#        configuration variables of its parent class,
#        if the configuration file does not exist a new one is created
#        by writing the default values of the configuration varibles to the file
#        Filename = parent_name.json
class config_file_reader(widget):

    #< path for config files
    config_path = "conf"

    #@brief constructor, reads in file
    def __init__(self):
        widget.__init__(self, "config_file_reader")
        self.__filename = config_file_reader.config_path + "/" + self.get_parent().name + ".json"
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
            self.log_warning("did not find : " + name)
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
        config_file_reader.__check_path()
        obj = self.get_parent()
        config_vars = obj.find_subinstances(None,
                lambda x: ( isinstance(x, config_var) ))
        new_data = dict()
        for key, obj in config_vars.iteritems():
            key = (lambda x: x if x.rfind(".") == -1 else x[x.rfind(".")+1:])(key)
            new_data[key] = obj.value
        with open(self.filename, "w") as f:
            json.dump(new_data, f)

    #check if config path exists and create if if it does not
    @staticmethod
    def __check_path():
        import os
        if not os.path.exists(config_file_reader.config_path):
            os.makedirs(config_file_reader.config_path)

    #@brief get filename
    #@return filename
    @property
    def filename(self):
        return self.__filename

    #@brief debug function, prints config vars
    def debug(self):
        if widget.debug == True:
            parent = self.get_parent()
            config_vars = parent.find_subinstances(None,
                lambda x: (isinstance(x, config_var)))
            for key, cvar in config_vars.iteritems():
                key = (lambda x: x if x.rfind(".") == -1 else x[x.rfind("."):])(key)
                self.log_debug("   "+key+" = "+str(cvar.get()))


class config_utils:
    @staticmethod
    def to_sec(time_str, err_val=0):
        factor = 1
        if time_str.find("s") != -1:
            time_str = time_str.replace("s","")
        elif time_str.find("m") != -1:
            time_str = time_str.replace("m","")
            factor = 60
        elif time_str.find("h") != -1:
            time_str = time_str.replace("h","")
            factor = 3600
        elif time_str.find("d") != -1:
            time_str = time_str.replace("d","")
            factor = 3600 * 24
        elif time_str.find("y") != -1:
            time_str = time_str.replace("y","")
            factor = 3600 * 24 * 365
        value = err_val
        try:
            value = int(time_str) * factor
        except ValueError:
            widget.log_static("could not convert "+time_str+" to int", "WARNING: config_utils.to_sec: ")
        return value
