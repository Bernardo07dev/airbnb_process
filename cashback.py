class Cashback():
      def __init__(self, account_id, payment_id, raw_value, due):
            self.account_id = account_id
            self.payment_id = payment_id
            self.cash_value = raw_value * 2 // 100
            self.due = due