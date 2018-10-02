import heroku3
from threading import Timer
import os

class restartingTimer:

    def __init__(self, interval):
        self.interval = interval
        self.timer = None
    
    def herokuDynoRestarter(self):

        heroku_conn = heroku3.from_key(os.environ["HEROKU_API_KEY"])
        app = heroku_conn.apps()['oft-irc-bot']
        app.restart()

    def start(self):
        self.timer = Timer(self.interval, self.herokuDynoRestarter)
        self.timer.start()

    def retsart(self):
        self.timer.cancel()
        self.timer = Timer(self.interval,self.herokuDynoRestarter)
        self.timer.start()
