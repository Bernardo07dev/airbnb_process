import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class Level1Tests(unittest.TestCase):
    """
    CodeSignal Level 1 Test Suite:
    - Account creation (`create_account`)
    - Deposits (`deposit`)
    - Transfers (`transfer`)
    """

    failureException = Exception

    def setUp(self):
        self.system = BankingSystemImpl()

    @timeout(0.4)
    def test_sample_1(self):
        self.assertTrue(self.system.create_account(1, "account1"))
        self.assertTrue(self.system.create_account(2, "account2"))
        self.assertEqual(self.system.deposit(3, "account1", 2000), 2000)
        self.assertEqual(self.system.deposit(4, "account2", 1000), 1000)
        self.assertEqual(self.system.transfer(5, "account1", "account2", 500), 1500)

    @timeout(0.4)
    def test_create_account_duplicate(self):
        self.assertTrue(self.system.create_account(10, "alice"))
        self.assertFalse(self.system.create_account(20, "alice"))
        self.assertTrue(self.system.create_account(30, "bob"))

    @timeout(0.4)
    def test_deposit_non_existing(self):
        self.assertIsNone(self.system.deposit(1, "ghost", 500))
        self.assertTrue(self.system.create_account(2, "alice"))
        self.assertEqual(self.system.deposit(3, "alice", 100), 100)
        self.assertEqual(self.system.deposit(4, "alice", 250), 350)

    @timeout(0.4)
    def test_transfer_failures(self):
        self.assertTrue(self.system.create_account(1, "acc1"))
        self.assertTrue(self.system.create_account(2, "acc2"))
        self.assertEqual(self.system.deposit(3, "acc1", 100), 100)

        # Same account
        self.assertIsNone(self.system.transfer(4, "acc1", "acc1", 50))
        # Non-existing source
        self.assertIsNone(self.system.transfer(5, "ghost", "acc2", 50))
        # Non-existing target
        self.assertIsNone(self.system.transfer(6, "acc1", "ghost", 50))
        # Insufficient funds
        self.assertIsNone(self.system.transfer(7, "acc1", "acc2", 150))
        # Valid transfer
        self.assertEqual(self.system.transfer(8, "acc1", "acc2", 100), 0)
        # Target now has funds to transfer back
        self.assertEqual(self.system.transfer(9, "acc2", "acc1", 40), 60)


if __name__ == "__main__":
    unittest.main()
