class Payment():
    def __init__(self, payment_id, account_id, amount, status="IN_PROGRESS"):
        self.payment_id = payment_id
        self.account_id = account_id
        self.amount = amount
        self.status = status
