class User:
  def __init__(self, id=-1, name='Unknown', conditions=[]):
    self.id = id
    self.name = name
    self.conditions = conditions
    self.decisions = []

  def print_me(self):
    print(self)

users = {}
users['1'] = User('1', 'Alice', [ 'hi_dose' ])
users['2'] = User('2', 'Bob', [ 'lo_dose' ])
users['3'] = User('3', 'Charlie', [ 'lo_dose' ])
users['4'] = User('4', 'Daisy', [ 'hi_dose' ])





  




