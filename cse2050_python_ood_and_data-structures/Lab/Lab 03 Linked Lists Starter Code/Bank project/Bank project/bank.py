from bankaccount import BankAccount
from bankit import BankIt
class Bank:
    def __init__(self):
        self._accounts = {}

    def addAccount(self, owner):
        self._accounts[owner] = BankAccount(owner, 0)

    def deposit(self, owner, amount):
        if self._findAccount(owner):
            self._accounts[owner].deposit(amount)
        else:
            raise Exception("Account number does not exist")

    def withdraw(self, owner, amount):
        self._accounts[owner].withdraw(amount)

    def getAccount(self, owner):
        return self._accounts[owner]

    def __iter__(self):
        return BankIt(self)

    def _findAccount(self, owner):
        return owner in self._accounts