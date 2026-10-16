import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class Level4Tests(unittest.TestCase):
    """
    CodeSignal Level 4 Test Suite:
    - Merging accounts (`merge_accounts`)
    - Historical balance queries (`get_balance`)
    - Forwarding pending cashbacks and payment statuses after merge
    - Lifecycle / existence windows and account re-creation
    """

    failureException = Exception

    def setUp(self):
        self.system = BankingSystemImpl()

    @timeout(0.4)
    def test_merge_accounts_validation(self):
        self.system.create_account(1, "alice")
        self.system.create_account(2, "bob")

        # Merge same account
        self.assertFalse(self.system.merge_accounts(3, "alice", "alice"))
        # Non-existing target
        self.assertFalse(self.system.merge_accounts(4, "ghost", "bob"))
        # Non-existing source
        self.assertFalse(self.system.merge_accounts(5, "alice", "ghost"))
        # Successful merge
        self.assertTrue(self.system.merge_accounts(6, "alice", "bob"))
        # Merged account cannot be merged again (it is deleted from active)
        self.assertFalse(self.system.merge_accounts(7, "alice", "bob"))

    @timeout(0.4)
    def test_merge_outgoing_and_cashback_forwarding(self):
        self.system.create_account(1, "alice")
        self.system.create_account(2, "bob")
        self.system.deposit(3, "alice", 1000)
        self.system.deposit(4, "bob", 1000)

        # Bob pays: 500. Cashback: 10 due at 86400005
        p_bob = self.system.pay(5, "bob", 500)
        self.assertEqual(p_bob, "payment1")

        # Merge bob into alice at timestamp 10
        self.assertTrue(self.system.merge_accounts(10, "alice", "bob"))

        # Payment status for Bob's payment should now work using 'alice'
        self.assertEqual(
            self.system.get_payment_status(15, "alice", "payment1"),
            "IN_PROGRESS"
        )
        # Using 'bob' directly fails because bob was merged away
        self.assertIsNone(self.system.get_payment_status(15, "bob", "payment1"))

        # Top spenders must aggregate outgoing from both
        self.assertEqual(self.system.top_spenders(20, 2), ["alice(500)"])

        # When cashback expires, it is refunded to alice
        # Alice had 1000 + 500 (bob's remaining) = 1500. With 10 cashback -> 1510
        self.assertEqual(
            self.system.get_payment_status(86400006, "alice", "payment1"),
            "CASHBACK_RECEIVED"
        )
        self.assertEqual(self.system.deposit(86400007, "alice", 0), 1510)

    @timeout(0.4)
    def test_get_balance_existence_and_history(self):
        self.system.create_account(10, "alice")
        self.system.deposit(20, "alice", 1000)
        self.system.create_account(30, "bob")
        self.system.deposit(40, "bob", 500)

        # Prior to creation -> None
        self.assertIsNone(self.system.get_balance(50, "alice", 5))
        # At creation before any deposit -> 0
        self.assertEqual(self.system.get_balance(50, "alice", 10), 0)
        # After deposit at 20 -> 1000
        self.assertEqual(self.system.get_balance(50, "alice", 25), 1000)

        # Merge bob into alice at 60
        self.system.merge_accounts(60, "alice", "bob")

        # Bob before merge -> historical balance is preserved
        self.assertEqual(self.system.get_balance(70, "bob", 45), 500)
        # Bob at or after merge -> None (removed)
        self.assertIsNone(self.system.get_balance(70, "bob", 60))
        self.assertIsNone(self.system.get_balance(70, "bob", 65))

        # Alice at 60 reflects merged total (1000 + 500 = 1500)
        self.assertEqual(self.system.get_balance(70, "alice", 60), 1500)

    @timeout(0.4)
    def test_account_recreation_after_merge(self):
        self.system.create_account(1, "alice")
        self.system.create_account(2, "bob")
        self.system.deposit(3, "bob", 400)
        self.system.merge_accounts(10, "alice", "bob")

        # Re-create bob at timestamp 20
        self.assertTrue(self.system.create_account(20, "bob"))

        # Prior to 10: old Bob
        self.assertEqual(self.system.get_balance(30, "bob", 5), 400)
        # Between 10 and 19: Bob did not exist
        self.assertIsNone(self.system.get_balance(30, "bob", 15))
        # At 20: new Bob starts with 0
        self.assertEqual(self.system.get_balance(30, "bob", 20), 0)


if __name__ == "__main__":
    unittest.main()
