from bank import Bank
bank = Bank()
bank.addAccount("123")
bank.addAccount("124")
bank.addAccount("125")
bank.deposit("123", 20)
bank.withdraw("123", 5)
for item in iter(bank):
    print(item.getOwner(), ":",  item.getBalance())

