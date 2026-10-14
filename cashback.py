class Cashback():
      def __init__(self, cashback_id, raw_value, status="IN_PROGRESS"):
            self.cashback_id = cashback_id
            self.raw_value = raw_value
            self.cash_value = raw_value * 0.02
            self.status = status