#!/usr/bin/python

from widget import widget

import threading

class timed_widget_update(object):
    def __init__(self, update_func, secs, *args, **kwargs):
        self.update_func = update_func
        self.secs = secs
        self.args = args
        self.kwargs = kwargs
        self.timer = None

    def __eq__(self, other):
        return self.update_func == other

    def set(self, secs, *args, **kwargs):
        self.secs = secs
        self.args = args
        self.kwargs = kwargs

    def start(self):
        if not self.timer == None:
            self.timer.cancel()
        if self.secs == 0:
            return
        self.timer = threading.Timer(self.secs, self.update)
        self.timer.start()

    def cancel(self):
        if self.timer == None:
            return
        self.timer.cancel()

    def update(self):
        self.update_func(*self.args, **self.kwargs)
        self.start()



class timed_widget(widget):
    def __init__(self, name):
        widget.__init__(self, name)
        self.updates = list()

    #TODO add random seconds? register_update_rnd
    #     for "big" updates
    def register_update(self, update_func, secs, *args, **kwargs):
        update = self.get_update(update_func)
        if not update == None:
            update.set(secs, *args, **kwargs)
        update = timed_widget_update(update_func, secs, *args, **kwargs)
        self.updates.append(update)

    def get_update(self, update_func):
        for update in self.updates:
            if update == update_func:
                return update
        return None

    def start(self):
        for update in self.updates:
            update.start()

    def start_update(self, update_func):
        update = self.get_update(update_func)
        if not update == None:
            update.start()

    def cancel_update(self, update_func):
        update = self.get_update(update_func)
        if not update == None:
            update.cancel()



