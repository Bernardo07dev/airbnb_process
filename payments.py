class Payment():
      def __init__(self, account_id, payment_id, value, cashback_id, status="IN_PROGRESS"):
            self.account_id = account_id
            self.payment_id = payment_id
            self.value = value
            self.cashback_id = cashback_id
            self.status = status