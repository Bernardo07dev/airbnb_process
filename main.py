from bank import *

my_bank = Bank()

my_bank.create_account(0, "1")
my_bank.create_account(0, "2")
my_bank.deposit(0, "2", 250)
print(my_bank.transfer(0, "2", "1", 550))
my_bank.print_acc()