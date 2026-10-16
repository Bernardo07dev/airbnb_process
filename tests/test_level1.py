import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class Level1Tests(unittest.TestCase):
    """
    The test class below includes 10 tests for Level 1.

    All have the same score.
    You are not allowed to modify this file,
    but feel free to read the source code
    to better understand what is happening in every specific case.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.system = BankingSystemImpl()

    @timeout(0.4)
    def test_level_1_case_01_basic_create(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertFalse(self.system.create_account(3, 'account1'))
        self.assertTrue(self.system.create_account(4, 'account3'))
        self.assertFalse(self.system.create_account(5, 'account2'))

    @timeout(0.4)
    def test_level_1_case_02_basic_deposit(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 1500), 1500)
        self.assertEqual(self.system.deposit(3, 'account1', 250), 1750)
        self.assertTrue(self.system.create_account(4, 'account2'))
        self.assertEqual(self.system.deposit(5, 'account2', 900), 900)
        self.assertEqual(self.system.deposit(6, 'account1', 50), 1800)

    @timeout(0.4)
    def test_level_1_case_03_deposit_to_non_existing_account(self):
        self.assertIsNone(self.system.deposit(1, 'account1', 100))
        self.assertTrue(self.system.create_account(2, 'account1'))
        self.assertIsNone(self.system.deposit(3, 'account2', 100))
        self.assertEqual(self.system.deposit(4, 'account1', 100), 100)
        self.assertFalse(self.system.create_account(5, 'account1'))
        self.assertEqual(self.system.deposit(6, 'account1', 1), 101)

    @timeout(0.4)
    def test_level_1_case_04_basic_transfer(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 2000), 2000)
        self.assertEqual(self.system.deposit(4, 'account2', 1000), 1000)
        self.assertEqual(self.system.transfer(5, 'account1', 'account2', 500), 1500)
        self.assertEqual(self.system.transfer(6, 'account2', 'account1', 1200), 300)
        self.assertEqual(self.system.deposit(7, 'account1', 100), 2800)
        self.assertEqual(self.system.deposit(8, 'account2', 100), 400)

    @timeout(0.4)
    def test_level_1_case_05_transfer_insufficient_funds(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 300), 300)
        self.assertIsNone(self.system.transfer(4, 'account1', 'account2', 301))
        self.assertEqual(self.system.transfer(5, 'account1', 'account2', 300), 0)
        self.assertIsNone(self.system.transfer(6, 'account1', 'account2', 1))
        self.assertEqual(self.system.transfer(7, 'account2', 'account1', 150), 150)
        self.assertEqual(self.system.deposit(8, 'account1', 10), 160)

    @timeout(0.4)
    def test_level_1_case_06_transfer_to_same_account(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 500), 500)
        self.assertIsNone(self.system.transfer(3, 'account1', 'account1', 100))
        self.assertIsNone(self.system.transfer(4, 'account1', 'account1', 1000))
        self.assertEqual(self.system.deposit(5, 'account1', 1), 501)

    @timeout(0.4)
    def test_level_1_case_07_transfer_non_existing_accounts(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 1000), 1000)
        self.assertIsNone(self.system.transfer(3, 'account1', 'account2', 100))
        self.assertIsNone(self.system.transfer(4, 'account2', 'account1', 100))
        self.assertIsNone(self.system.transfer(5, 'account3', 'account2', 10))
        self.assertTrue(self.system.create_account(6, 'account2'))
        self.assertEqual(self.system.transfer(7, 'account1', 'account2', 100), 900)
        self.assertEqual(self.system.deposit(8, 'account2', 5), 105)

    @timeout(0.4)
    def test_level_1_case_08_mixed_operations(self):
        self.assertTrue(self.system.create_account(1, 'alice'))
        self.assertTrue(self.system.create_account(2, 'bob'))
        self.assertTrue(self.system.create_account(3, 'carol'))
        self.assertFalse(self.system.create_account(4, 'bob'))
        self.assertEqual(self.system.deposit(5, 'alice', 5000), 5000)
        self.assertEqual(self.system.deposit(6, 'bob', 3000), 3000)
        self.assertEqual(self.system.transfer(7, 'alice', 'bob', 1500), 3500)
        self.assertEqual(self.system.transfer(8, 'bob', 'carol', 4500), 0)
        self.assertIsNone(self.system.transfer(9, 'bob', 'alice', 1))
        self.assertEqual(self.system.deposit(10, 'carol', 500), 5000)
        self.assertEqual(self.system.transfer(11, 'carol', 'alice', 2500), 2500)
        self.assertIsNone(self.system.deposit(12, 'dave', 100))
        self.assertEqual(self.system.transfer(13, 'alice', 'carol', 6000), 0)
        self.assertEqual(self.system.deposit(14, 'alice', 1), 1)
        self.assertEqual(self.system.deposit(15, 'bob', 20), 20)
        self.assertIsNone(self.system.transfer(16, 'carol', 'carol', 1))
        self.assertEqual(self.system.deposit(17, 'carol', 1500), 10000)

    @timeout(0.4)
    def test_level_1_case_09_transfer_chain(self):
        for i in range(1, 7):
            self.assertTrue(self.system.create_account(i, f'acc_{i}'))
        self.assertFalse(self.system.create_account(7, 'acc_3'))
        self.assertEqual(self.system.deposit(8, 'acc_1', 100), 100)
        self.assertEqual(self.system.deposit(9, 'acc_2', 200), 200)
        self.assertEqual(self.system.deposit(10, 'acc_3', 300), 300)
        self.assertEqual(self.system.deposit(11, 'acc_4', 400), 400)
        self.assertEqual(self.system.deposit(12, 'acc_5', 500), 500)
        self.assertEqual(self.system.deposit(13, 'acc_6', 600), 600)
        self.assertEqual(self.system.transfer(14, 'acc_6', 'acc_5', 600), 0)
        self.assertEqual(self.system.transfer(15, 'acc_5', 'acc_4', 1100), 0)
        self.assertEqual(self.system.transfer(16, 'acc_4', 'acc_3', 1500), 0)
        self.assertEqual(self.system.transfer(17, 'acc_3', 'acc_2', 1800), 0)
        self.assertEqual(self.system.transfer(18, 'acc_2', 'acc_1', 2000), 0)
        self.assertEqual(self.system.deposit(19, 'acc_1', 900), 3000)
        self.assertIsNone(self.system.transfer(20, 'acc_6', 'acc_1', 1))

    @timeout(0.4)
    def test_level_1_case_10_case_sensitive_ids_and_large_timestamps(self):
        self.assertTrue(self.system.create_account(1, 'Account1'))
        self.assertTrue(self.system.create_account(2, 'account1'))
        self.assertEqual(self.system.deposit(1000000, 'Account1', 700), 700)
        self.assertEqual(self.system.deposit(2000000, 'account1', 300), 300)
        self.assertEqual(self.system.transfer(3000000, 'account1', 'Account1', 300), 0)
        self.assertEqual(self.system.deposit(4000000, 'Account1', 1), 1001)
        self.assertIsNone(self.system.transfer(999999999, 'ACCOUNT1', 'account1', 1))


if __name__ == '__main__':
    unittest.main()
