from bank import *

my_bank = Bank()

my_bank.create_account(1, "alice")
my_bank.create_account(2, "bob")

my_bank.deposit(3, "alice", 2000)
my_bank.deposit(4, "bob", 2000)

print(my_bank.pay(5, "alice", 500))
print(my_bank.pay(6, "bob", 1000))
print(my_bank.pay(7, "ghost", 100))
print(my_bank.pay(8, "alice", 900))

my_bank.print_acc()

print(my_bank.get_payment_status(9, "alice", "payment1"))
print(my_bank.get_payment_status(10, "bob", "payment2"))
print(my_bank.get_payment_status(11, "alice", "payment2"))
print(my_bank.get_payment_status(12, "ghost", "payment1"))
print(my_bank.get_payment_status(13, "alice", "payment99"))

print(my_bank.top_spenders(14, 2))

print(my_bank.get_payment_status(86400005, "alice", "payment5"))
print(my_bank.get_payment_status(86400006, "bob", "payment2"))

print(my_bank.deposit(86400007, "alice", 0))
print(my_bank.deposit(86400008, "bob", 0))

print(my_bank.top_spenders(86400009, 2))


print(my_bank.pay(86400010, "alice", 500))
print(my_bank.get_payment_status(86400011, "alice", "payment5"))
print(my_bank.get_payment_status(86400012, "bob", "payment6"))
my_bank.print_acc()
