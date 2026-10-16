import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class Level3Tests(unittest.TestCase):
    """
    CodeSignal Level 3 Test Suite:
    - Payments (`pay`) with global IDs and 2% cashback
    - Delayed cashback after 86,400,000 ms
    - Payment status inspection (`get_payment_status`)
    - Integration with `top_spenders`
    """

    failureException = Exception

    def setUp(self):
        self.system = BankingSystemImpl()

    @timeout(0.4)
    def test_payment_ids_and_failures(self):
        self.system.create_account(1, "alice")
        self.system.create_account(2, "bob")
        self.system.deposit(3, "alice", 1000)

        # Non-existing account
        self.assertIsNone(self.system.pay(4, "ghost", 100))
        # Insufficient funds
        self.assertIsNone(self.system.pay(5, "alice", 2000))

        # First successful pay gets payment1
        self.assertEqual(self.system.pay(6, "alice", 400), "payment1")
        # Second successful pay gets payment2 (global counter)
        self.system.deposit(7, "bob", 500)
        self.assertEqual(self.system.pay(8, "bob", 200), "payment2")

        # Top spenders must include payments
        self.assertEqual(
            self.system.top_spenders(9, 2),
            ["alice(400)", "bob(200)"]
        )

    @timeout(0.4)
    def test_cashback_timing_and_refund(self):
        self.system.create_account(1, "alice")
        self.system.deposit(2, "alice", 1000)

        # Withdraw 500 at timestamp 100
        # Cashback = 500 * 0.02 = 10. Due at 100 + 86400000 = 86400100
        p_id = self.system.pay(100, "alice", 500)
        self.assertEqual(p_id, "payment1")

        # Status before 24h
        self.assertEqual(
            self.system.get_payment_status(200, "alice", "payment1"),
            "IN_PROGRESS"
        )
        # Invalid account or invalid payment lookup
        self.assertIsNone(self.system.get_payment_status(200, "ghost", "payment1"))
        self.assertIsNone(self.system.get_payment_status(200, "alice", "payment99"))

        # Right before cashback expiration
        self.assertEqual(
            self.system.get_payment_status(86400099, "alice", "payment1"),
            "IN_PROGRESS"
        )

        # Exactly at or after due timestamp
        self.assertEqual(
            self.system.get_payment_status(86400100, "alice", "payment1"),
            "CASHBACK_RECEIVED"
        )

        # Balance reflects refunded cashback: 500 remaining + 10 cashback = 510
        # Deposit 0 to observe balance after cashback processed
        self.assertEqual(self.system.deposit(86400101, "alice", 0), 510)


if __name__ == "__main__":
    unittest.main()
