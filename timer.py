import time
from threading import Timer


def display(msg):
    print(msg + ' ' + time.strftime('%H:%M:%S'))


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
            print(' ')


# We are now creating a thread timer and controling it
timer = RepeatTimer(1, display, [''])
timer.start()  # recalling run
print('Threading started')
time.sleep(10)  # It gets suspended for the given number of seconds
timer.cancel()
print('Threading finishing')
