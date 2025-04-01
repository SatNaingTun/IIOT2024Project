# RepeatedTimer.py
import threading


class RepeatedTimer(object):
    stopCode = False

    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        return self.function(*self.args, **self.kwargs)

    def start(self):

        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            if (self.stopCode == False):
                self._timer.start()
            else:
                self._timer.stop()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
