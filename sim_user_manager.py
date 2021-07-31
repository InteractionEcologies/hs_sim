from datetime import datetime
import json


class User:
    def __init__(self, jsonObj):
        self.id = jsonObj['id']
        self.name = jsonObj['name']
        self.conditions = jsonObj['conditions']
        self.params = {}
        self.params['message_times'] = jsonObj['message_times']
        self.decisions = []
        if 'decisions' in jsonObj: 
            self.decisions = jsonObj['decisions']
            for d in self.decisions:
                d['decision_time'] = datetime.strptime(d['decision_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                d['timestamp'] = datetime.strptime(d['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def __repr__(self):
        s = '\n'
        s += self.name + ', id: ' + self.id
        s += ', conditions: ' + self.conditions.__repr__()
        s += ', params: ' + self.params.__repr__()
        return s

class UserManager:

    def __init__(self):
        self.load_users()

    def load_users(self):
        self.users = {}
        f = open('test_users.json')
        test_user_dicts = json.load(f)['users']
        for ud in test_user_dicts:
            u = User(ud)
            self.users[u.id] = u

    def get_users(self):
        return self.users