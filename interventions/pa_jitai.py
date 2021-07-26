import random
from datetime import datetime
import json

def choose_action(user, curr_time):
  decision = None

  print('choosing action for', user.name, 'params:', user.params)

  # Figure out what message time slots exist for today
  message_times = user.params['message_times']
  todays_times = []
  for mt in message_times.values():
    mt_split = mt.split(':')
    t = datetime(curr_time.year, curr_time.month, curr_time.day, int(mt_split[0]), int(mt_split[1])) 
    todays_times.append(t)

  # Find the most recent message time slot today
  # Note that there might not be any yet (if it's too early)
  min_time = datetime(1970, 10, 6)
  most_recent_message_time_slot = min_time
  for tt in todays_times:
    if tt <= curr_time:
      most_recent_message_time_slot = tt
  if (most_recent_message_time_slot == min_time):
    print("Too early, go back to sleep")
    return None  

  print("Current time:", curr_time)
  print("Most recent time:" , most_recent_message_time_slot)

  # Find the decision_time of the most recent decision made for this user
  # Note that no decisions might have been made yet
  decisions = user.decisions
  latest_decision_time = None
  if len(decisions) > 0:
    latest_decision = decisions[-1]
    latest_decision_time = latest_decision['decision_time']
    print("Latest decision made:", latest_decision_time)
  
  # it is time to make a decision if there is a message time that is 
  # earlier than now for which no decision has been made
  if (latest_decision_time == most_recent_message_time_slot):
    print('decision was already made')
    return None
  
  print('decision needs to be made, making it')

  r = random.random()
  if (r < 0.5):
    decision = {
      "type": "message_sent",
      "message_id": "pa_msg_1",
      "decision_time": latest_decision_time,
      "timestamp": curr_time    
    }
  else:
    decision = {
      "type": "no_action",
      "decision_time": latest_decision_time,
      "timestamp": curr_time    
    }
  return decision # None if no action was taken

############## TESTING BELOW ########################

class User:
  def __init__(self, id=-1, name='Unknown', conditions=[], jsonObj=None):
    if jsonObj:
      self.id = jsonObj['id']
      self.name = jsonObj['name']
      self.conditions = jsonObj['conditions']
      self.params = {}
      self.params['message_times'] = jsonObj['message_times']
      self.decisions = []
      if 'decisions' in jsonObj: 
        self.decisions = jsonObj['decisions']
    else:
      self.id = id
      self.name = name
      self.conditions = conditions
      self.decisions = []

  def print_me(self):
    print(self)

def self_test():
  # set up users
  f = open('test_users.json')
  test_users = json.load(f)['users']
  users = {}
  for u in test_users:
    if 'decisions' in u:
      for d in u['decisions']:
        d['decision_time'] = datetime.strptime(d['decision_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        d['timestamp'] = datetime.strptime(d['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    users[u['id']] = User(jsonObj=u)
  print(users)

  ## test 1: 
  ##   user: "1" 
  ##   latest decision "2021-08-01T10:30:00.000Z"
  ##   next decision time "2021-08-01T13:00:00.000Z"
  ##   current time "2021-08-01T11:30:00.000Z"
  ##   result: no decision
  curr_time = datetime(2021, 8, 1, 11, 30)
  print(users['1'], curr_time)
  action = choose_action(users['1'], curr_time)
  print(action)

  ## test 2:
  ##   user: "1" 
  ##   latest decision "2021-08-01T10:30:00.000Z"
  ##   next decision time "2021-08-01T13:00:00.000Z"
  ##   current time "2021-08-01T13:05:00.000Z"
  ##   result: some decision
  curr_time = datetime(2021, 8, 1, 13, 5)
  print(users['1'], curr_time)
  action = choose_action(users['1'], curr_time)
  print(action)

  ## test 3: 
  ##   user: "2" 
  ##   latest decision None
  ##   next decision time "2021-08-01T08:00:00.000Z"
  ##   current time "2021-08-01T06:05:00.000Z"
  ##   result: no decision
  curr_time = datetime(2021, 8, 1, 6, 5)
  print(users['2'], curr_time)
  action = choose_action(users['2'], curr_time)
  print(action)

  ## test 4: 
  ##   user: "2" 
  ##   latest decision None
  ##   next decision time "2021-08-01T08:00:00.000Z"
  ##   current time "2021-08-01T08:05:00.000Z"
  ##   result: some decision
  curr_time = datetime(2021, 8, 1, 8, 5)
  print(users['2'], curr_time)
  action = choose_action(users['2'], curr_time)
  print(action)




if __name__ == "__main__":
  self_test()
