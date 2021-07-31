
from datetime import datetime, timedelta
from event_manager import EventManager


'''
Clock:
    A simulated clock that just cranks through times with no pause from
    a start time to end time with the specified increment 
'''
START_TIME = datetime(2021, 1, 1, 0, 0)
END_TIME = datetime(2021, 1, 2, 0, 0)
INCREMENT = 5

class Clock:

    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.start_time = START_TIME
        self.end_time = END_TIME
        self.increment = timedelta(minutes=INCREMENT)
        self.curr_time = self.start_time
        
    def start(self):
        while self.curr_time < self.end_time:
            self.event_manager.do_tick(self.curr_time)
            self.curr_time += self.increment

    def get_time(self):
        return self.curr_time

