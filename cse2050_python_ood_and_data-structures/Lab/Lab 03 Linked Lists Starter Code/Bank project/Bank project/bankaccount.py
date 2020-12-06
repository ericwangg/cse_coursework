class BankAccount:

  def __init__(self, owner, balance):
    self._owner = owner
    self._balance = balance

  def  deposit(self, amount):
    self._balance += amount

  def  withdraw(self, amount):
       self._balance -= amount

  def  getBalance(self):
       return self._balance
  def getOwner(self):
      return self._owner

