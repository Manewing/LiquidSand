#!/usr/bin/python

from widget import widget

class gui(widget):
    def __init__(self, name):
        widget.__init__(self, name)
        self.log_debug("init gui done")
        # TODO
