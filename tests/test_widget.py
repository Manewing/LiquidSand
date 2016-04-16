#!/usr/bin/python

import sys
sys.path.append("../liquidsand/base/")

from widget import widget

class deep(widget):
    def __init__(self, name):
        widget.__init__(self, name)
        self.log("so deep")

class deep_sub(deep):
  def __init__(self, name, value):
      self.value = value
      widget.__init__(self, name)
      self.log("so much deeper")

class test(widget):
    def __init__(self, name):
        widget.__init__(self, name)
        self.log("test")
        self.d = deep("deep")

class system(widget):
  def __init__(self, name):
      widget.__init__(self, name)
      self.t1 = test("test1")
      self.t2 = test("test2")
      self.d = deep("deep")

if __name__ == "__main__":
    sys = system("system")
    sys.d.add(deep_sub, "deep_sub", 5)
    print(sys.name)
    print(sys.t1.name)
    print(sys.t2.name)
    print(sys.d.name)
    print(sys.t1.d.name)
    print(sys.t2.d.name)
    print(sys.d.deep_sub.name)
    print(sys.d.deep_sub.value)
    t1 = widget.get("system.test1")
    print(t1)
