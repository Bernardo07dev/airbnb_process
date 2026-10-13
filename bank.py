
from account import Account

class Bank():
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, timestamp, account_id):
        if account_id in self.accounts.keys():
            return False
        else:
            self.accounts[account_id] = Account(account_id)
            return True
    
    def deposit(self, timestamp, account_id, amount):
        pass

    def print_acc(self):
        for ac in self.accounts.values():
            print(ac.__dict__)