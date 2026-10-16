from cashback import Cashback
from payment import Payment
from collections import deque
from account import Account
from banking_system import BankingSystem

class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.accounts = {} #ACC_COUNT: Obj(Account)
        self.actives = {} # ACCOUNT_ID: ACC_COUNT
        self.payments = {}
        self.cashbacks = deque()
        self.p_count = 1
        self.acc_count = 0

    #===---===---===---===---===---===---LEVEL 1---===---===---===---===---===---===
    #create_account
    def create_account(self, timestamp: int, account_id: str) -> bool:
        self.check_cashbacks(timestamp)
        acc = self.get_acc(account_id)
        if not acc:
            self.acc_count += 1
            self.actives[account_id] = self.acc_count
            self.accounts[self.acc_count] = Account(account_id, timestamp)
            return True
        return False

    #deposit
    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self.check_cashbacks(timestamp)
        acc = self.get_acc(account_id)
        if not acc:
            return None
        acc.balance += amount
        acc.history.append((timestamp, acc.balance))
        return acc.balance

    #transfer
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        self.check_cashbacks(timestamp)
        s_acc = self.get_acc(source_account_id)
        t_acc = self.get_acc(target_account_id)

        if source_account_id == target_account_id or not s_acc or not t_acc or s_acc.balance < amount:
            return None
        
        s_acc.balance -= amount
        s_acc.outgoing += amount
        t_acc.balance += amount

        s_acc.history.append((timestamp, s_acc.balance))
        t_acc.history.append((timestamp, t_acc.balance))

        return s_acc.balance

    #===---===---===---===---===---===---LEVEL 2---===---===---===---===---===---===
    #top_spenders
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        self.check_cashbacks(timestamp)
        def sort_acc(acc_id):
            acc = self.get_acc(acc_id)
            return (-acc.outgoing, acc.account_id)

        sorted_acc = sorted(self.actives, key=sort_acc)
        output = [f"{acc}({self.get_acc(acc).outgoing})" for acc in sorted_acc]

        return output[0:n]

    #===---===---===---===---===---===---LEVEL 3---===---===---===---===---===---===
    #pay
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        self.check_cashbacks(timestamp)
        acc = self.get_acc(account_id)

        if not acc or acc.balance < amount:
            return None
        
        acc.balance -= amount
        acc.outgoing += amount

        p_id = f"payment{self.p_count}"
        self.payments[p_id] = Payment(p_id, account_id, amount)
        self.cashbacks.append(Cashback(p_id, account_id, amount, timestamp))
        self.p_count += 1

        acc.history.append((timestamp, acc.balance))

        return p_id
    
    #get_payment_status
    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        self.check_cashbacks(timestamp)
        acc = self.get_acc(account_id)

        if not acc or payment not in self.payments or self.payments[payment].account_id != account_id:
            return None
        
        return self.payments[payment].status

    #===---===---===---===---===---===---LEVEL 4---===---===---===---===---===---===
    #merge_accounts
    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        self.check_cashbacks(timestamp)
        acc_active = self.get_acc(account_id_1)
        acc_merged = self.get_acc(account_id_2)

        if account_id_1 == account_id_2 or not acc_active or not acc_merged:
            return False
        
        #Balance add
        acc_active.balance += acc_merged.balance

        #Outgoing add
        acc_active.outgoing += acc_merged.outgoing

        #Change cashbacks
        for c in self.cashbacks:
            if not self.cashbacks:
                break
            if c.account_id == account_id_2:
                c.account_id = account_id_1
        
        #Update payments
        for p in self.payments.values():
            if not self.payments:
                break
            if p.account_id == account_id_2:
                 p.account_id = account_id_1 

        #Atualizar history
        acc_active.history.append((timestamp, acc_active.balance))
        
        #Remove account
        acc_merged.removed = timestamp
        self.actives.pop(account_id_2)

        return True
    
    #get_balance
    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        self.check_cashbacks(timestamp)
        for acc in self.accounts.values():
            if acc.account_id == account_id and acc.created <= time_at:
                if not acc.removed or acc.removed > time_at:
                    last_h = acc.history[0]
                    for h in acc.history:
                        if h[0] > time_at:
                            return last_h[1]
                        last_h = h
                    return last_h[1]
        return None
        

    #===---===---===---===---===---===---HELPERS---===---===---===---===---===---===
    def get_acc(self, acc_id):
        acc = self.actives.get(acc_id)
        if not acc:
            return acc
        return self.accounts[acc]

    def check_cashbacks(self, timestamp: int):
        while self.cashbacks and self.cashbacks[0].due <= timestamp:
            cash = self.cashbacks[0]

            acc = self.get_acc(cash.account_id)
            acc.balance += cash.cash_value
            self.payments[cash.payment_id].status = "CASHBACK_RECEIVED"

            acc.history.append((cash.due, acc.balance))

            self.cashbacks.popleft()