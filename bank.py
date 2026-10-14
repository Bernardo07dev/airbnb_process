from account import Account
from payments import Payment

class Bank():
    def __init__(self):
        self.accounts = {}
        self.payments = {}
        self.cashbacks = {}
    
    def create_account(self, timestamp, account_id):
        if account_id in self.accounts:
            return False
        else:
            self.accounts[account_id] = Account(account_id)
            return True
    
    def deposit(self, timestamp, account_id, amount):
        if account_id not in self.accounts:
            return None
        self.accounts[account_id].balance += amount
        return self.accounts[account_id].balance

    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        if source_account_id == target_account_id or source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        if self.accounts[source_account_id].balance < amount:
            return None
        
        self.accounts[source_account_id].balance -= amount
        self.accounts[source_account_id].outgoing += amount
        self.accounts[target_account_id].balance += amount

        return self.accounts[source_account_id].balance

    def top_spenders(self, timestamp: int, n: int):
        def ac_sort(acc):
            return (-acc.outgoing, acc.account_id)

        sort_list = sorted(self.accounts.values(), key=ac_sort)

        final_list = [f"{x.account_id}({x.outgoing})" for x in sort_list]


        return final_list[0:n]

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        if account_id not in self.accounts or self.accounts[account_id].balance < amount:
            return None

        self.accounts[account_id].balance -= amount
        self.accounts[account_id].outgoing -= amount

        self.payments[f"payment{timestamp}"] = Payment(self.accounts[account_id], f"payment{timestamp}", amount, "IN_PROGRESS", timestamp)

    def print_acc(self):
        for ac in self.accounts.values():
            print("Contas")
            print(ac.__dict__)

        for pg in self.payments.values():    
            print("Pagamentos")
            print(pg.__dict__)