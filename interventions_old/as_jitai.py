import random

def choose_action(user, curr_time):
  decision = None
  r = random.random()
  if (r < 0.05):
    decision = {
      "action": {
        "notes": "YES!!",
        "id": r
      }
    }

  if (r > 0.95):
    decision = {
      "action": {
        "notes": "no :(",
        "id": r
      }
    }
  return decision # None if no action was taken


class Main:
  pass

  def say_hi():
    print("Hi from", __name__)

def say_hi():
  print("Hi from", __name__)
