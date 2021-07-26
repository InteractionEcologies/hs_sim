from datetime import datetime, date, time, timezone, timedelta

class EventManager:
  def __init__(self, study_manager):  
    self.start_time = datetime(2021, 1, 1, 0, 0)
    self.end_time = datetime(2021, 1, 2, 0, 0)
    self.heartbeat = timedelta(minutes=5)
    self.curr_time = self.start_time
    self.study_manager = study_manager


  def run(self):
    while self.curr_time < self.end_time:
      self.study_manager.do_tick(self.curr_time)
      self.curr_time += self.heartbeat


