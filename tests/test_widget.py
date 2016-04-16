#!/usr/bin/python

import sys
sys.path.append("../liquidsand/base/")

from widget import widget

class deep(widget):
    def __init__(self, name):
        widget.__init__(self, name)
        self.log("so deep")

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

if __name__ == "__main__":
    sys = system("system")
    print(sys.name)
    print(sys.t1.name)
    print(sys.t2.name)
    print(sys.t1.d.name)
    print(sys.t2.d.name)
    t1 = widget.get("system.test1")
    print(t1)
