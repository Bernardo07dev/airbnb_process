import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class Level4Tests(unittest.TestCase):
    """
    The test class below includes 10 tests for Level 4.

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
    def test_level_4_case_01_basic_merge(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 1000), 1000)
        self.assertEqual(self.system.deposit(4, 'account2', 500), 500)
        self.assertTrue(self.system.merge_accounts(5, 'account1', 'account2'))
        self.assertEqual(self.system.deposit(6, 'account1', 100), 1600)
        self.assertIsNone(self.system.deposit(7, 'account2', 100))
        self.assertEqual(self.system.top_spenders(8, 2), ['account1(0)'])

    @timeout(0.4)
    def test_level_4_case_02_merge_invalid(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertFalse(self.system.merge_accounts(3, 'account1', 'account1'))
        self.assertFalse(self.system.merge_accounts(4, 'account1', 'account3'))
        self.assertFalse(self.system.merge_accounts(5, 'account3', 'account2'))
        self.assertTrue(self.system.merge_accounts(6, 'account1', 'account2'))
        self.assertFalse(self.system.merge_accounts(7, 'account1', 'account2'))
        self.assertFalse(self.system.merge_accounts(8, 'account2', 'account1'))

    @timeout(0.4)
    def test_level_4_case_03_merge_outgoing(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertTrue(self.system.create_account(3, 'account3'))
        self.assertEqual(self.system.deposit(4, 'account1', 1000), 1000)
        self.assertEqual(self.system.deposit(5, 'account2', 1000), 1000)
        self.assertEqual(self.system.deposit(6, 'account3', 1000), 1000)
        self.assertEqual(self.system.transfer(7, 'account1', 'account3', 100), 900)
        self.assertEqual(self.system.transfer(8, 'account2', 'account3', 300), 700)
        self.assertEqual(self.system.pay(9, 'account2', 200), 'payment1')
        self.assertEqual(
            self.system.top_spenders(10, 3),
            ['account2(500)', 'account1(100)', 'account3(0)']
        )
        self.assertTrue(self.system.merge_accounts(11, 'account3', 'account2'))
        self.assertEqual(
            self.system.top_spenders(12, 3),
            ['account3(500)', 'account1(100)']
        )
        self.assertEqual(self.system.transfer(13, 'account3', 'account1', 100), 1800)
        self.assertEqual(
            self.system.top_spenders(14, 2),
            ['account3(600)', 'account1(100)']
        )

    @timeout(0.4)
    def test_level_4_case_04_merge_with_pending_cashback(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 1000), 1000)
        self.assertEqual(self.system.deposit(4, 'account2', 1000), 1000)
        self.assertEqual(self.system.pay(5, 'account2', 500), 'payment1')
        self.assertTrue(self.system.merge_accounts(6, 'account1', 'account2'))
        self.assertEqual(self.system.get_payment_status(7, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertIsNone(self.system.get_payment_status(8, 'account2', 'payment1'))
        self.assertEqual(self.system.get_payment_status(86400005, 'account1', 'payment1'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.deposit(86400006, 'account1', 1), 1511)

    @timeout(0.4)
    def test_level_4_case_05_basic_get_balance(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 1000), 1000)
        self.assertTrue(self.system.create_account(3, 'account2'))
        self.assertEqual(self.system.deposit(4, 'account2', 500), 500)
        self.assertEqual(self.system.transfer(10, 'account1', 'account2', 300), 700)
        self.assertIsNone(self.system.get_balance(20, 'account1', 0))
        self.assertEqual(self.system.get_balance(21, 'account1', 1), 0)
        self.assertEqual(self.system.get_balance(22, 'account1', 2), 1000)
        self.assertEqual(self.system.get_balance(23, 'account1', 9), 1000)
        self.assertEqual(self.system.get_balance(24, 'account1', 10), 700)
        self.assertEqual(self.system.get_balance(25, 'account2', 3), 0)
        self.assertEqual(self.system.get_balance(26, 'account2', 10), 800)
        self.assertIsNone(self.system.get_balance(27, 'account2', 2))
        self.assertEqual(self.system.get_balance(28, 'account1', 28), 700)

    @timeout(0.4)
    def test_level_4_case_06_get_balance_after_merge(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 1000), 1000)
        self.assertTrue(self.system.create_account(3, 'account2'))
        self.assertEqual(self.system.deposit(4, 'account2', 500), 500)
        self.assertTrue(self.system.merge_accounts(20, 'account1', 'account2'))
        self.assertEqual(self.system.get_balance(25, 'account2', 4), 500)
        self.assertEqual(self.system.get_balance(26, 'account2', 19), 500)
        self.assertIsNone(self.system.get_balance(27, 'account2', 20))
        self.assertEqual(self.system.get_balance(28, 'account1', 19), 1000)
        self.assertEqual(self.system.get_balance(29, 'account1', 20), 1500)
        self.assertIsNone(self.system.get_balance(30, 'account2', 25))

    @timeout(0.4)
    def test_level_4_case_07_get_balance_with_cashback(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 1000), 1000)
        self.assertEqual(self.system.pay(100, 'account1', 500), 'payment1')
        self.assertEqual(self.system.deposit(200, 'account1', 100), 600)
        self.assertEqual(self.system.get_balance(86400200, 'account1', 86400099), 600)
        self.assertEqual(self.system.get_balance(86400201, 'account1', 86400100), 610)
        self.assertEqual(self.system.get_balance(86400202, 'account1', 150), 500)
        self.assertEqual(self.system.get_balance(86400203, 'account1', 100), 500)
        self.assertEqual(self.system.get_balance(86400204, 'account1', 99), 1000)

    @timeout(0.4)
    def test_level_4_case_08_recreate_account_after_merge(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account2', 400), 400)
        self.assertEqual(self.system.pay(4, 'account2', 100), 'payment1')
        self.assertTrue(self.system.merge_accounts(10, 'account1', 'account2'))
        self.assertTrue(self.system.create_account(20, 'account2'))
        self.assertEqual(self.system.deposit(21, 'account2', 50), 50)
        self.assertIsNone(self.system.get_payment_status(22, 'account2', 'payment1'))
        self.assertEqual(self.system.get_payment_status(23, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_balance(30, 'account2', 5), 300)
        self.assertEqual(self.system.get_balance(31, 'account2', 3), 400)
        self.assertIsNone(self.system.get_balance(32, 'account2', 15))
        self.assertEqual(self.system.get_balance(33, 'account2', 20), 0)
        self.assertEqual(self.system.get_balance(34, 'account2', 21), 50)
        self.assertEqual(
            self.system.top_spenders(35, 2),
            ['account1(100)', 'account2(0)']
        )
        self.assertEqual(self.system.deposit(86400004, 'account2', 1), 51)
        self.assertEqual(self.system.deposit(86400005, 'account1', 1), 303)

    @timeout(0.4)
    def test_level_4_case_09_chained_merges(self):
        self.assertTrue(self.system.create_account(1, 'A'))
        self.assertTrue(self.system.create_account(2, 'B'))
        self.assertTrue(self.system.create_account(3, 'C'))
        self.assertEqual(self.system.deposit(4, 'A', 100), 100)
        self.assertEqual(self.system.deposit(5, 'B', 200), 200)
        self.assertEqual(self.system.deposit(6, 'C', 300), 300)
        self.assertEqual(self.system.pay(10, 'B', 100), 'payment1')
        self.assertTrue(self.system.merge_accounts(20, 'A', 'B'))
        self.assertTrue(self.system.merge_accounts(30, 'C', 'A'))
        self.assertEqual(self.system.get_payment_status(31, 'C', 'payment1'), 'IN_PROGRESS')
        self.assertIsNone(self.system.get_payment_status(32, 'A', 'payment1'))
        self.assertIsNone(self.system.get_payment_status(33, 'B', 'payment1'))
        self.assertEqual(self.system.top_spenders(34, 3), ['C(100)'])
        self.assertEqual(self.system.get_balance(40, 'A', 25), 200)
        self.assertIsNone(self.system.get_balance(41, 'A', 30))
        self.assertEqual(self.system.get_balance(42, 'B', 15), 100)
        self.assertEqual(self.system.get_balance(43, 'C', 30), 500)
        self.assertEqual(self.system.deposit(86400010, 'C', 1), 503)
        self.assertEqual(self.system.get_payment_status(86400011, 'C', 'payment1'), 'CASHBACK_RECEIVED')

    @timeout(0.4)
    def test_level_4_case_10_mixed_operations(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertTrue(self.system.create_account(3, 'account3'))
        self.assertEqual(self.system.deposit(4, 'account1', 2000), 2000)
        self.assertEqual(self.system.deposit(5, 'account2', 3000), 3000)
        self.assertEqual(self.system.deposit(6, 'account3', 4000), 4000)
        self.assertEqual(self.system.pay(7, 'account1', 1000), 'payment1')
        self.assertEqual(self.system.pay(8, 'account2', 500), 'payment2')
        self.assertEqual(self.system.transfer(9, 'account3', 'account1', 1500), 2500)
        self.assertTrue(self.system.merge_accounts(10, 'account2', 'account1'))
        self.assertTrue(self.system.create_account(11, 'account1'))
        self.assertEqual(self.system.deposit(12, 'account1', 10), 10)
        self.assertEqual(
            self.system.top_spenders(13, 3),
            ['account2(1500)', 'account3(1500)', 'account1(0)']
        )
        self.assertEqual(self.system.get_balance(14, 'account1', 9), 2500)
        self.assertIsNone(self.system.get_balance(15, 'account1', 10))
        self.assertEqual(self.system.get_balance(16, 'account1', 11), 0)
        self.assertEqual(self.system.get_balance(17, 'account2', 10), 5000)
        self.assertEqual(self.system.get_payment_status(18, 'account2', 'payment1'), 'IN_PROGRESS')
        self.assertIsNone(self.system.get_payment_status(19, 'account1', 'payment1'))
        self.assertEqual(self.system.deposit(86400008, 'account3', 1), 2501)
        self.assertEqual(self.system.get_balance(86400009, 'account2', 86400007), 5020)
        self.assertEqual(self.system.get_balance(86400010, 'account2', 86400008), 5030)
        self.assertEqual(self.system.get_balance(86400011, 'account1', 86400008), 10)
        self.assertEqual(self.system.get_balance(86400012, 'account2', 9), 2500)


if __name__ == '__main__':
    unittest.main()
