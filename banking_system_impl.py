from banking_system import BankingSystem
from account import Account
from cashback import Cashback
from payment import Payment
from collections import deque

class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.accounts = {} # acc_count: Account()
        self.actives = {} # account_id: acc_count
        self.payments = {}
        self.cashbacks = deque()
        self.acc_count = 1
        self.p_count = 1

    #---+++---+++------+++---+++---LEVLE 1---+++---+++------+++---+++---
    def create_account(self, timestamp: int, account_id: str) -> bool:
        self.check_cashbacks(timestamp)
        acc = self.get_acc(account_id)
        if acc:
            return False

        self.actives[account_id] = self.acc_count
        self.accounts[self.acc_count] = Account(account_id, timestamp)
        self.acc_count += 1
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self.check_cashbacks(timestamp)
        acc = self.get_acc(account_id)
        if not acc:
            return None

        acc.balance += amount
        acc.history.append((timestamp, acc.balance))
        return acc.balance

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        self.check_cashbacks(timestamp)
        if source_account_id == target_account_id:
            return None
        
        s_acc = self.get_acc(source_account_id)
        t_acc = self.get_acc(target_account_id)

        if not (s_acc and t_acc) or s_acc.balance < amount:
            return None

        s_acc.balance -= amount
        s_acc.outgoing += amount

        t_acc.balance += amount

        s_acc.history.append((timestamp, s_acc.balance))
        t_acc.history.append((timestamp, t_acc.balance))

        return s_acc.balance

    #---+++---+++------+++---+++---LEVLE 2---+++---+++------+++---+++---
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        self.check_cashbacks(timestamp)
        def sort_acc(active_acc):
            acc = self.accounts[self.actives[active_acc]]
            return (-acc.outgoing, acc.account_id)

        sorted_acc = sorted(self.actives, key=sort_acc)
        formated = [f"{acc}({self.accounts[self.actives[acc]].outgoing})" for acc in sorted_acc]

        return formated[0:n]

    #---+++---+++------+++---+++---LEVLE 3---+++---+++------+++---+++---
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        self.check_cashbacks(timestamp)
        acc = self.get_acc(account_id)
        if not acc or acc.balance < amount:
            return None

        acc.balance -= amount
        acc.outgoing += amount

        p_id = f"payment{self.p_count}"
        self.payments[p_id] = Payment(account_id, amount)
        self.cashbacks.append(Cashback(p_id, account_id, amount, timestamp))
        self.p_count += 1

        acc.history.append((timestamp, acc.balance))
        return p_id

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        self.check_cashbacks(timestamp)
        acc = account_id
        if payment not in self.payments or not acc or self.payments[payment].account_id != account_id:
            return None

        return self.payments[payment].status

    #---+++---+++------+++---+++---LEVLE 4---+++---+++------+++---+++---
    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        self.check_cashbacks(timestamp)
        if account_id_1 == account_id_2:
            return False

        active_acc = self.get_acc(account_id_1)
        merged_acc = self.get_acc(account_id_2)

        if not (active_acc and merged_acc):
            return False

        #Balance changing
        active_acc.balance += merged_acc.balance

        #Outgoing changing
        active_acc.outgoing += merged_acc.outgoing

        #Loop Cashbacks
        for cash in self.cashbacks:
            if cash.account_id == account_id_2:
                cash.account_id = account_id_1

        #Loops Payments
        for pay in self.payments.values():
            if pay.account_id == account_id_2:
                pay.account_id = account_id_1

        #History in Active
        active_acc.history.append((timestamp, active_acc.balance))

        #Remove from actives
        merged_acc.removed = timestamp
        self.actives.pop(account_id_2)
        return True

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        self.check_cashbacks(timestamp)
        for acc in self.accounts.values():
            if acc.account_id == account_id and (not acc.removed or time_at < acc.removed) and acc.created <= time_at:
                last_h = acc.history[0][1]
                for h in acc.history:
                    if h[0] > time_at:
                        return last_h
                    last_h = h[1]
                return last_h
        return None


    #---+++---+++---+++---HELPERS---+++---+++---+++---
    def get_acc(self, account_id):
        acc = self.actives.get(account_id)
        if not acc:
            return acc

        return self.accounts[acc]

    def check_cashbacks(self, timestamp):
        while self.cashbacks and self.cashbacks[0].due_date <= timestamp:
            self.payments[self.cashbacks[0].payment_id].status = "CASHBACK_RECEIVED"
            acc = self.get_acc(self.cashbacks[0].account_id)
            if acc:
                acc.balance += self.cashbacks[0].cash_value
                acc.history.append((self.cashbacks[0].due_date, acc.balance))
            self.cashbacks.popleft()