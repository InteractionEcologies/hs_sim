from datetime import datetime, timedelta

class Trigger:
  pass

class EventManager:
  def __init__(self, study_manager):  
    self.start_time = datetime(2021, 1, 1, 0, 0)
    self.end_time = datetime(2021, 1, 2, 0, 0)
    self.heartbeat = timedelta(minutes=5)
    self.curr_time = self.start_time
    self.study_manager = study_manager
    self.triggers = []
    self.decision_records = []

  def register_trigger(self, trigger: Trigger) -> None:
    # add trigger to triggers
    self.triggers.append(trigger)
    
  def unregister_trigger(self, trigger: Trigger) -> None:
    # remove triggers from triggers
    self.triggers.remove(trigger)

  def do_tick(self, current_datetime: datetime) -> None:
    print('doing tick', current_datetime)
    for t in self.triggers:
      if t.should_fire(current_datetime):
        dr = t.perform_action(current_datetime)
        self.decision_records.append(dr)
        print(dr)
        
        