class Account():
    def __init__(self, account_id, created, removed=None):
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0
        self.created = created
        self.removed = removed
        self.history = [(created, 0)]