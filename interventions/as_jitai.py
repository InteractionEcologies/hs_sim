
from datetime import datetime, timedelta
from enum import Enum
from random import random
import json
import sys

sys.path.append('..') ## make sure parent directory is in the python path
from event_manager import EventManager
from sim_user_manager import User

INTERVENTION_ID = 'as_jitai'
class ACTION_TYPES(Enum):
    NO_ACTION = 'NO_ACTION'
    MESSAGE_SENT = 'MESSAGE_SENT'


class ASDecisionRecord:
    pass

'''
ASTrigger:
    An implementation of the Trigger interface for a trigger managed by ASIntervention

    The trigger is long-lived and compares the user's current sedentary time with a threshhold
    to determine whether to fire. It also keeps track of the last time it fired and compares with 
    an "inter-message" threshhold to determine whether to fire, in order to suppress exessive
    messaging.
'''
class ASTrigger:
    def __init__(self, intervention, trigger_time: datetime):
        pass

    def should_fire(self, current_datetime: datetime) -> bool:
        return False
        
    def perform_action(self, current_datetime: datetime) -> ASDecisionRecord: 
        return None

'''
ASIntervention:
    An implementation of the Intervention interface for an anti-sedentary messaging intervention
    that probabilistically sends a message when a user has been sedentary for a specified period of time

    This intervention creates one long-lived Trigger that always checks the user's current sedentary time
'''
class ASIntervention:
    def __init__(self, event_manager, user: User, current_datetime: datetime = datetime.now()):
        pass

    def do_action(self, current_datetime: datetime, trigger) -> ASDecisionRecord:
        return None

    def get_next_trigger(self, current_datetime: datetime):
        pass

def init_intervention(event_manager: EventManager, 
                      user: User,
                      current_datetime: datetime = datetime.now()):
    return ASIntervention(event_manager, user, current_datetime)