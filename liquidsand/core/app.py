#!/usr/bin/python

import sys
sys.path.append("liquidsand/base/")

from timed_widget import timed_widget

class app(timed_widget):
  def __init__(self, name):
      timed_widget.__init__(self, name)
