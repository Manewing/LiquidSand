#!/usr/bin/python

import inspect

#@class meta widget
#@brief provides hook to call finalize after __init__ of derived class
class meta_widget(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.finalize()
        return obj

#@class widget
#@brief Adds a hierachie system to classes. Each widget has a
#       name, which consists of a basename and its actual name
#       "basename.act_name". Every widget is identfiable by its name.
#       To provide hierachie widgets need to be created in the constructor of
#       an other widget or by calling add on the parent widget
class widget(object):
    #< all widget instances
    __instances = dict()
    #< current base(name) level
    __base_level = ""

    #set meta class
    __metaclass__ = meta_widget

    #@brief constructor creates new widget at current hierachie level
    #@param name - name of the widget
    def __init__(self, name):
        name = name.replace(".", "");
        self.__name = widget.__get_name(name)
        self.__sub_instances = dict()
        self.__add_instance()
        widget.__add_base_level(name)

    #@brief get called after init of widget, reset basename level
    def finalize(self):
        widget.__remove_base_level()

    #@brief create and add new widget to this widget (also as attribute)
    #@param cls   - class of widget to create
    #@param name  - name of new widget
    #@param *args - additional arguments
    def add(self, cls, name, *args):
      base_level = widget.__base_level
      widget.__base_level = self.name
      obj = cls(name, *args)
      setattr(self, name, obj)
      __base_level = base_level


    #@brief get hierachie name
    #@param name - widget name
    #@return hierachie name
    @staticmethod
    def __get_name(name):
        if widget.__base_level == "":
            return name
        return widget.__base_level + "." + name

    #@brief get base name from name
    #@param name - hierachie name
    #@return widget name
    @staticmethod
    def get_base_name(name):
        if name == "" or name.rfind(".") == -1:
            return name
        return name[:name.rfind(".")]

    #@brief adds a base name level
    #@brief level - base name level to add
    @staticmethod
    def __add_base_level(level):
        if widget.__base_level == "":
            widget.__base_level = level
            return
        widget.__base_level = widget.__base_level + "." + level

    #@brief removes last base name level
    @staticmethod
    def __remove_base_level():
        widget.__base_level = widget.get_base_name(widget.__base_level)

    #@brief widget registers itself by its parent and by the widget class
    def __add_instance(self):
        if widget.__instances.get(self.name) != None:
            # TODO generate random string?
            self.log_error("<- instance(name) already exits")
        else:
            widget.__instances[self.name] = self
        obj = widget.get(widget.get_base_name(self.name))
        if obj == None or obj.__sub_instances.get(self.name) != None:
            # TODO generate random string?
            self.log_error("<- instance(name) already exits")
        else:
            obj.__sub_instances[self.name] = self

    #@brief get name
    #@return hierachie name of widget
    @property
    def name(self):
        return self.__name

    #@brief get parent instance
    #@return instance of parent or None
    def get_parent(self):
        return widget.get(widget.get_base_name(self.name))

    #@brief Find sub instances of widget, keys (names) and values (widgets)
    #       are compared by the compare function. Only if both functions
    #       return True on comparision a subinstance is "found".
    #@param key_cmp - compare function for keys
    #@param val_cmp - compare function for values
    #@return dict of all sub instances keys: (names) values: (widgets)
    def find_subinstances(self, key_cmp, val_cmp):
      if key_cmp == None:
        key_cmp = lambda x: ( True )
      if val_cmp == None:
        val_cmp = lambda x: ( True )
      subinstances = dict()
      for key, val in self.__sub_instances.iteritems():
          if key_cmp(key) and val_cmp(val):
              subinstances[key] = val
      return subinstances


    #@brief get widget by name
    #@param name - hierachical name
    #@return if found the widget else None
    @staticmethod
    def get(name):
        if widget.__instances.has_key(name) == True:
            return widget.__instances[name]
        widget.log_static(name + " does not exist", "ERROR: ")
        return None

    #@brief write to log
    #@param log    - log text to log
    #@param prefix - prefix for log text
    @staticmethod
    def log_static(log, prefix=""):
        #TODO add log file
        print(prefix + log)

    #@brief write to log (widget name is logged)
    #@param log    - log text to log
    #@param prefix - prefix for log text
    def log(self, log, prefix=""):
        widget.log_static(log, prefix + self.name + ": ")

    #@brief log a warning (widget name is logged)
    #@param waring - warning text to log
    def log_warning(self, warning):
        self.log(warning, "WARNING: ")

    #@brief log a error (widget name is logged)
    #@param error - error text to log
    def log_error(self, error):
        self.log(error, "ERROR: ")
