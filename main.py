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

print("\n--- TESTES LEVEL 4 ---")
print("1. Antes da criação (esperado None):", my_bank.get_balance(100, "alice", 0))
print("2. No instante da criação (esperado 0):", my_bank.get_balance(100, "alice", 1))
print("3. Após depósito tempo 3 (esperado 2000):", my_bank.get_balance(100, "alice", 3))
print("4. Após pay tempo 5 (esperado 1500):", my_bank.get_balance(100, "alice", 5))

print("\nExecutando merge_accounts(90000000, 'alice', 'bob')...")
print("Merge realizado:", my_bank.merge_accounts(90000000, "alice", "bob"))

print("5. Bob antes do merge em tempo 86400006 (esperado 1020):", my_bank.get_balance(90000001, "bob", 86400006))
print("6. Bob a partir do merge em tempo 90000000 (esperado None):", my_bank.get_balance(90000001, "bob", 90000000))
print("7. Alice após o merge em tempo 90000000 (esperado 1148):", my_bank.get_balance(90000001, "alice", 90000000))
