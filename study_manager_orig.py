import json
import importlib
import os

import user_manager
from event_manager import EventManager

class StudyManager:

  def __init__(self):
    self.studytudy = {}
    self.users = {}
    self.interventions = {}
    
    self.import_interventions()
    self.init_study()
    self.init_users()

  def import_interventions(self):
    cwd = os.getcwd()
    cwd = cwd + '/interventions'
    iv_names = []
    for name in os.listdir(cwd):
      if name.endswith(".py") and not name.startswith("__"):
        name = name[:-3]
        iv_names.append(name)

    for name in iv_names:
      module_name = 'interventions.' + name
      self.interventions[name] = importlib.import_module(module_name)

  def init_user(self, user):
    params = {}
    iv_names = set()
    
    for iv in self.study['all_conditions']['interventions']:
      iv_names.add(iv["name"])
      up = iv['user_params']
      for param in up:
        pname = param["name"]
        pvalue = param["default_value"]
        params[pname] = pvalue

    user_conds = user.conditions
    for ucond in user_conds:
      for study_cond in self.study['conditions']:
        scond = study_cond["name"]
        if ucond == scond:
          for iv in study_cond['interventions']:
            iv_names.add(iv["name"])
            up = iv['user_params']
            for param in up:
              pname = param["name"]
              pvalue = param["default_value"]
              params[pname] = pvalue

    user.params = params
    user.interventions = iv_names

  def init_users(self):
    # use hardcoded users for now
    hc_users = user_manager.users
    print(hc_users)
    for id in hc_users:
      user = hc_users[id]
      self.init_user(user)
    self.users = hc_users

  def init_study(self):
    f = open('studyconfig.json')
    study_config = json.load(f)
    self.study = study_config['study']

  def do_tick(self, curr_time):
    # for each user
    for u in self.users:
      user = self.users[u]
      # collect context variables
      # context_manager.get_context_for_user(user)

      # figure out which interventions are active
      for i_name in user.interventions:
        i = self.interventions[i_name]
        # ask each intervention to choose action
        decision = i.choose_action(user, curr_time)
        if decision:
          user.decisions.append((i_name, decision))

if __name__ == "__main__":
  sm = StudyManager()
  em = EventManager(sm)
  em.run()
  users = sm.users
  # for u in users:
  #   print('*' * 30)
  #   print(u)
  #   print('*' * 30)
  #   print(users[u].decisions)
