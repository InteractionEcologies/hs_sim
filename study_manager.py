import json
import importlib
import os

from event_manager import EventManager
from sim_clock import Clock
from sim_user_manager import UserManager

class StudyManager:

  def __init__(self):
    self.user_manager = UserManager()
    self.event_manager = EventManager(self)
    self.clock = Clock(self.event_manager)

    self.study = {}
    self.interventions = {}
    self.users = {}

    self.init_study()
    self.init_users()
    
  def start(self):
    self.clock.start()
  
  def init_study(self):
    f = open('studyconfig.json')
    study_config = json.load(f)
    self.study = study_config['study']
    self.import_interventions()

  def init_users(self):
    self.user_manager.load_users()
    self.users = self.user_manager.get_users()
    for u in self.users.values():
      self.init_user(u)

  def init_user(self, user):

    user_params = {}
    iv_names = set()

    # add all of the default interventions (ones that apply to all users)
    for iv in self.study['all_conditions']['interventions']:
      iv_name = iv['name'] # grab the intevention name
      all_cond_iv_params = iv['user_params'] # grab the intervention-specific parameters
      iv_names.add(iv_name) # add to the set, avoid dupes later
      user_params[iv_name] = {} # create a location in user_params for iv_params

      # construct each param with default value and add it to user_params
      for param in all_cond_iv_params:
        pname = param['name']
        pvalue = param['default_value']
        user_params[iv_name][pname] = pvalue

    # go through all of this user's conditions and reger to the 
    # study's conditions to figure out what parameters to add/set/override
    for ucond in user.conditions: # this user's conditions
      for study_cond in self.study['conditions']: # the study's conditions
        scond = study_cond['name']

        # figure out which condition(s) this user is in
        if ucond == scond:
          for iv in study_cond['interventions']: # these will all apply to the user
            iv_name = iv["name"]
            iv_names.add(iv_name) # add to the set, will avoid dupes
            cond_iv_params = iv['user_params'] # grab the intervention-specific parameters

            if not iv_name in user_params: # if needed, create a loction in user_params for iv_params
              user_params[iv_name] = {}

            for param in cond_iv_params:
              pname = param["name"]
              pvalue = param["default_value"]
              user_params[iv_name][pname] = pvalue

    user.params = user_params

    # initialize this user's interventions, save the intervention objects with the user
    user.interventions = []
    for iv in iv_names:
      iv_obj = self.interventions[iv].init_intervention(self.event_manager, user, self.clock.get_time())
      user.interventions.append(iv_obj)

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

if __name__ == "__main__":
  sm = StudyManager()
  sm.start()
  

