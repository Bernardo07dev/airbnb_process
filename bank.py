from collections import deque
from account import Account
from payments import Payment
from cashback import Cashback

class Bank():
    def __init__(self):
        self.accounts = {}
        self.payments = {}
        self.cashbacks = deque()
        self.p_count = 0
    
    def create_account(self, timestamp, account_id):
        self.cashback_desc(timestamp)
        if account_id in self.accounts:
            return False
        else:
            self.accounts[account_id] = Account(account_id)
            return True
    
    def deposit(self, timestamp, account_id, amount):
        self.cashback_desc(timestamp)
        if account_id not in self.accounts:
            return None
        self.accounts[account_id].balance += amount
        return self.accounts[account_id].balance

    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        self.cashback_desc(timestamp)
        if source_account_id == target_account_id or source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        if self.accounts[source_account_id].balance < amount:
            return None
        
        self.accounts[source_account_id].balance -= amount
        self.accounts[source_account_id].outgoing += amount
        self.accounts[target_account_id].balance += amount

        return self.accounts[source_account_id].balance

    def top_spenders(self, timestamp: int, n: int):
        self.cashback_desc(timestamp)
        def ac_sort(acc):
            return (-acc.outgoing, acc.account_id)

        sort_list = sorted(self.accounts.values(), key=ac_sort)

        final_list = [f"{x.account_id}({x.outgoing})" for x in sort_list]


        return final_list[0:n]

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        self.cashback_desc(timestamp)
        if account_id not in self.accounts or self.accounts[account_id].balance < amount:
            return None

        self.accounts[account_id].balance -= amount
        self.accounts[account_id].outgoing += amount

        self.p_count += 1

        self.payments[f"payment{self.p_count}"] = Payment(self.accounts[account_id].account_id, f"payment{self.p_count}", amount, timestamp)
        self.cashbacks.append(Cashback(account_id, f"payment{self.p_count}", amount, timestamp + 86400000))
        return f"payment{self.p_count}"

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        self.cashback_desc(timestamp)
        if account_id not in self.accounts or payment not in self.payments or self.payments[payment].account_id != account_id:
            return None

        return self.payments[payment].status

    def cashback_desc(self, timestamp):
        while self.cashbacks and self.cashbacks[0].due <= timestamp:
            self.payments[self.cashbacks[0].payment_id].status = "CASHBACK_RECEIVED"
            self.accounts[self.cashbacks[0].account_id].balance += self.cashbacks[0].cash_value
            self.cashbacks.popleft()


    def print_acc(self):
        print("Contas")
        for ac in self.accounts.values():
            print(ac.__dict__)

        print("")

        print("Pagamentos")
        for pg in self.payments.values():    
            print(pg.__dict__)

        print("")

        print("Cashbacks")
        for pg in self.cashbacks:    
            print(pg.__dict__)