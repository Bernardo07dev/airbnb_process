
from account import Account

class Bank():
    def __init__(self):
        self.accounts = {}
    
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
        self.accounts[target_account_id].balance += amount

        return self.accounts[source_account_id].balance

    def print_acc(self):
        for ac in self.accounts.values():
            print(ac.__dict__)