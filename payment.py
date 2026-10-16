class Payment():
      def __init__(self, account_id, amount, status="IN_PROGRESS"):
            self.account_id = account_id
            self.amount = amount
            self.status = status