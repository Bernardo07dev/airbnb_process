class Cashback():
      def __init__(self, payment_id, account_id, amount, timestamp):
            self.payment_id = payment_id
            self.account_id = account_id
            self.cash_value = int(amount * 0.02)
            self.due_date = timestamp + 86400000