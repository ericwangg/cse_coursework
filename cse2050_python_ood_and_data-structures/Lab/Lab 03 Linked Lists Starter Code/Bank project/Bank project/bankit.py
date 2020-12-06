class BankIt:
    def __init__(self, bank):
        self._bank = bank
        self._it = iter(bank._accounts)

    def __next__(self):
        return self._bank.getAccount(next(self._it))

    def __iter__(self):
        return self