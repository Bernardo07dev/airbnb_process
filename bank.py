from collections import deque
from account import Account
from payments import Payment
from cashback import Cashback

class Bank():
    def __init__(self):
        self.instances = {}
        self.active = {}
        self.payments = {}
        self.cashbacks = deque()
        self.p_count = 0
        self.inst_count = 0
    
    def create_account(self, timestamp, account_id):
        self.cashback_desc(timestamp)
        if self.acc(account_id):
            return False
        else:
            self.inst_count += 1
            self.instances[self.inst_count] = Account(account_id, self.inst_count, timestamp, )
            self.active[account_id] = self.inst_count
            return True
    
    def deposit(self, timestamp, account_id, amount):
        self.cashback_desc(timestamp)
        acc = self.acc(account_id)
        if not acc:
            return None
        acc.balance += amount
        acc.history.append((timestamp, acc.balance))
        return acc.balance

    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        self.cashback_desc(timestamp)
        if source_account_id == target_account_id:
            return None
        
        s_acc = self.acc(source_account_id)
        t_acc = self.acc(target_account_id)

        if not s_acc or not t_acc:
            return None
        if s_acc.balance < amount:
            return None
        
        s_acc.balance -= amount
        s_acc.outgoing += amount
        s_acc.history.append((timestamp, s_acc.balance))
        
        t_acc.balance += amount
        t_acc.history.append((timestamp, t_acc.balance))


        return s_acc.balance

    def top_spenders(self, timestamp: int, n: int):
        self.cashback_desc(timestamp)
        def ac_sort(acc):
            return (-acc.outgoing, acc.account_id)

        valid_acc = [self.instances[i] for i in self.active.values()]

        sort_list = sorted(valid_acc, key=ac_sort)

        final_list = [f"{x.account_id}({x.outgoing})" for x in sort_list]


        return final_list[0:n]

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        self.cashback_desc(timestamp)

        acc = self.acc(account_id)
        if not acc or acc.balance < amount:
            return None

        acc.balance -= amount
        acc.outgoing += amount

        acc.history.append((timestamp, acc.balance))

        self.p_count += 1

        self.payments[f"payment{self.p_count}"] = Payment(account_id, f"payment{self.p_count}", amount, timestamp)
        self.cashbacks.append(Cashback(account_id, f"payment{self.p_count}", amount, timestamp + 86400000))
        return f"payment{self.p_count}"

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        self.cashback_desc(timestamp)

        acc = self.acc(account_id)
        if not acc or payment not in self.payments or self.payments[payment].account_id != account_id:
            return None

        return self.payments[payment].status

    def cashback_desc(self, timestamp):
        while self.cashbacks and self.cashbacks[0].due <= timestamp:
            self.payments[self.cashbacks[0].payment_id].status = "CASHBACK_RECEIVED"
            acc = self.acc(self.cashbacks[0].account_id)
            if acc:
                acc.balance += self.cashbacks[0].cash_value
                acc.history.append((self.cashbacks[0].due, acc.balance))
            self.cashbacks.popleft()

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        self.cashback_desc(timestamp)

        if account_id_1 == account_id_2:
            return False

        active_acc = self.acc(account_id_1)
        merged_acc = self.acc(account_id_2)

        if not active_acc or not merged_acc:
            return False

        for c in self.cashbacks:
            if c.account_id == account_id_2:
                c.account_id = account_id_1

        for p in self.payments.values():
            if p.account_id == account_id_2:
                p.account_id = account_id_1

        # Removing Merged From active
        self.active.pop(account_id_2)
        # Update Balance
        active_acc.balance += merged_acc.balance
        active_acc.history.append((timestamp, active_acc.balance))
        # Update Outgoing
        active_acc.outgoing += merged_acc.outgoing
        merged_acc.removed = timestamp

        return True

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
    

    #============HELPER============
    def acc(self, account_id):
        active = self.active.get(account_id)
        if not active:
            return active
        return self.instances[active]


    def print_acc(self):
        print("Contas")
        for ac in self.instances.values():
            print(ac.__dict__)

        print("")

        print("Pagamentos")
        for pg in self.payments.values():    
            print(pg.__dict__)

        print("")

        print("Cashbacks")
        for pg in self.payments.values():    
            print(pg.__dict__)