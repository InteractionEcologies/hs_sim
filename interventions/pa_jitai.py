
from datetime import datetime, timedelta
from enum import Enum
from random import random
import json
import sys
sys.path.append('..') ## make sure parent directory is in the python path
from event_manager import EventManager
from sim_user_manager import User

INTERVENTION_ID = 'pa_jitai'
class ACTION_TYPES(Enum):
    NO_ACTION = 'NO_ACTION'
    MESSAGE_SENT = 'MESSAGE_SENT'

'''
PATrigger:
    An implementation of the Trigger interface for a triggers managed by PAIntervention

    The trigger looks compares it's "go time" with the current time to decide whether or not to fire
'''
class PATrigger:
    def __init__(self, 
                 intervention, 
                 trigger_time: datetime):
        self.intervention = intervention
        self.trigger_time = trigger_time

    def should_fire(self, current_datetime: datetime) -> bool:
        print('PATrigger.should_fire() for ', self.intervention.user.name, current_datetime, self.trigger_time, current_datetime > self.trigger_time)
        return current_datetime > self.trigger_time
        
    def perform_action(self, current_datetime: datetime):
        return self.intervention.do_action(current_datetime, self)
    

class PADecisionRecord:
    def __init__(self, 
                 decision_time: datetime,
                 decision_type: str,
                 decision_details: dict):
        self.intervention_id = INTERVENTION_ID
        self.decision_time = decision_time
        self.decicion_type = decision_type
        self.decision_details = decision_details

'''
PAIntervention:
    An implementation of the Intervention interface for a physical activity-promoting intervention
    that sends messages probabilistically at specified times of day (specified in User.getUserParams())

    This intervention ensures that only one of its Triggers is registered at a time--the Trigger 
    corresponsing to the *next* message decision time
'''
class PAIntervention:
    def __init__(self, 
                 event_manager: EventManager, 
                 user: User, 
                 current_datetime: datetime = datetime.now()):
        self.event_manager = event_manager
        self.user = user
        self.message_probability = user.params[INTERVENTION_ID]['message_probability']
        init_trigger = self.get_next_trigger(current_datetime)
        event_manager.register_trigger(init_trigger)

    def do_action(self,
                  current_datetime: datetime, 
                  trigger: PATrigger) -> PADecisionRecord:
        self.event_manager.unregister_trigger(trigger)
        self.event_manager.register_trigger(self.get_next_trigger(current_datetime))

        if random() < self.message_probability:
            # choose the message (TBD)
            # send the message (TBD)
            # record the decision
            return PADecisionRecord(trigger.trigger_time,
                                    ACTION_TYPES.MESSAGE_SENT,
                                    {"message_id": "ALWAYS_BLUE",
                                     "user": self.user})
        else:
            return PADecisionRecord(trigger.trigger_time,
                                    ACTION_TYPES.NO_ACTION,
                                    {})

    def get_next_trigger(self, current_datetime: datetime):
        print('pa_jitai.get_next_trigger(), current_datetime:', current_datetime)
        message_times = self.user.params[INTERVENTION_ID]['message_times']
        for mt in message_times.values():
            hours = mt.split(':')[0]
            minutes = mt.split(':')[1]
            t = datetime(current_datetime.year, 
                         current_datetime.month, 
                         current_datetime.day, 
                         int(hours), 
                         int(minutes))
            if (t > current_datetime):
                print('next', t)
                return PATrigger(self, t)

        # if we get here, we need to look at tomorrow
        tomorrow = current_datetime + timedelta(days=1)
        mt = list(message_times.values())[0]
        hours = mt.split(':')[0]
        minutes = mt.split(':')[1]
        t = datetime(tomorrow.year, 
                     tomorrow.month, 
                     tomorrow.day, 
                     int(hours), 
                     int(minutes))
        print('next', t)
        return PATrigger(self, t)

def init_intervention(event_manager: EventManager, 
                      user: User,
                      current_datetime: datetime = datetime.now()):
    return PAIntervention(event_manager, user, current_datetime)

if __name__ == "__main__":
    pai = PAIntervention(None, None, None)
    pai.get_next_trigger(datetime.now())
    pai.get_next_trigger(datetime(2021, 8, 1, 13, 0))
    pai.get_next_trigger(datetime(2021, 8, 1, 22, 0))
