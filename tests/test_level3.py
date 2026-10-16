import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class Level3Tests(unittest.TestCase):
    """
    The test class below includes 10 tests for Level 3.

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
    def test_level_3_case_01_basic_pay(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 1000), 1000)
        self.assertEqual(self.system.pay(3, 'account1', 300), 'payment1')
        self.assertEqual(self.system.pay(4, 'account1', 200), 'payment2')
        self.assertEqual(self.system.deposit(5, 'account1', 100), 600)

    @timeout(0.4)
    def test_level_3_case_02_pay_failures(self):
        self.assertIsNone(self.system.pay(1, 'account1', 100))
        self.assertTrue(self.system.create_account(2, 'account1'))
        self.assertIsNone(self.system.pay(3, 'account1', 1))
        self.assertEqual(self.system.deposit(4, 'account1', 500), 500)
        self.assertIsNone(self.system.pay(5, 'account1', 501))
        self.assertEqual(self.system.pay(6, 'account1', 500), 'payment1')
        self.assertIsNone(self.system.pay(7, 'account1', 1))
        self.assertIsNone(self.system.pay(8, 'account2', 1))

    @timeout(0.4)
    def test_level_3_case_03_global_payment_counter(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 1000), 1000)
        self.assertEqual(self.system.deposit(4, 'account2', 1000), 1000)
        self.assertEqual(self.system.pay(5, 'account1', 100), 'payment1')
        self.assertEqual(self.system.pay(6, 'account2', 100), 'payment2')
        self.assertIsNone(self.system.pay(7, 'account2', 5000))
        self.assertEqual(self.system.pay(8, 'account1', 100), 'payment3')
        self.assertIsNone(self.system.pay(9, 'account3', 1))
        self.assertEqual(self.system.pay(10, 'account2', 100), 'payment4')

    @timeout(0.4)
    def test_level_3_case_04_cashback_timing(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 1000), 1000)
        self.assertEqual(self.system.pay(10, 'account1', 500), 'payment1')
        self.assertEqual(self.system.deposit(86400009, 'account1', 100), 600)
        self.assertEqual(self.system.deposit(86400010, 'account1', 100), 710)
        self.assertEqual(self.system.deposit(86400011, 'account1', 1), 711)

    @timeout(0.4)
    def test_level_3_case_05_payment_status(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 1000), 1000)
        self.assertEqual(self.system.pay(3, 'account1', 100), 'payment1')
        self.assertEqual(self.system.get_payment_status(4, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(86400002, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(86400003, 'account1', 'payment1'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400004, 'account1', 'payment1'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.deposit(86400005, 'account1', 1), 903)

    @timeout(0.4)
    def test_level_3_case_06_payment_status_invalid(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 1000), 1000)
        self.assertEqual(self.system.pay(4, 'account1', 100), 'payment1')
        self.assertIsNone(self.system.get_payment_status(5, 'account2', 'payment1'))
        self.assertIsNone(self.system.get_payment_status(6, 'account1', 'payment2'))
        self.assertIsNone(self.system.get_payment_status(7, 'account3', 'payment1'))
        self.assertEqual(self.system.get_payment_status(8, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertIsNone(self.system.pay(9, 'account2', 1))
        self.assertIsNone(self.system.get_payment_status(10, 'account2', 'payment2'))

    @timeout(0.4)
    def test_level_3_case_07_cashback_rounding(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 10000), 10000)
        self.assertEqual(self.system.pay(3, 'account1', 49), 'payment1')
        self.assertEqual(self.system.pay(4, 'account1', 50), 'payment2')
        self.assertEqual(self.system.pay(5, 'account1', 149), 'payment3')
        self.assertEqual(self.system.pay(6, 'account1', 1001), 'payment4')
        self.assertEqual(self.system.deposit(7, 'account1', 1), 8752)
        self.assertEqual(self.system.deposit(86400100, 'account1', 1), 8776)
        self.assertEqual(self.system.get_payment_status(86400101, 'account1', 'payment1'), 'CASHBACK_RECEIVED')

    @timeout(0.4)
    def test_level_3_case_08_top_spenders_with_payments(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertTrue(self.system.create_account(3, 'account3'))
        self.assertEqual(self.system.deposit(4, 'account1', 1000), 1000)
        self.assertEqual(self.system.deposit(5, 'account2', 1000), 1000)
        self.assertEqual(self.system.deposit(6, 'account3', 1000), 1000)
        self.assertEqual(self.system.pay(7, 'account1', 300), 'payment1')
        self.assertEqual(self.system.transfer(8, 'account2', 'account3', 200), 800)
        self.assertEqual(self.system.pay(9, 'account2', 150), 'payment2')
        self.assertEqual(self.system.pay(10, 'account3', 1200), 'payment3')
        self.assertEqual(
            self.system.top_spenders(11, 3),
            ['account3(1200)', 'account2(350)', 'account1(300)']
        )
        self.assertEqual(
            self.system.top_spenders(86400011, 3),
            ['account3(1200)', 'account2(350)', 'account1(300)']
        )
        self.assertEqual(self.system.deposit(86400012, 'account3', 1), 25)

    @timeout(0.4)
    def test_level_3_case_09_multiple_pending_cashbacks(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 10000), 10000)
        self.assertEqual(self.system.pay(1000, 'account1', 1000), 'payment1')
        self.assertEqual(self.system.pay(2000, 'account1', 2000), 'payment2')
        self.assertEqual(self.system.pay(3000, 'account1', 3000), 'payment3')
        self.assertEqual(self.system.get_payment_status(86401500, 'account1', 'payment1'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86401600, 'account1', 'payment2'), 'IN_PROGRESS')
        self.assertEqual(self.system.deposit(86401700, 'account1', 1), 4021)
        self.assertEqual(self.system.deposit(86405000, 'account1', 1), 4122)
        self.assertEqual(self.system.get_payment_status(86405001, 'account1', 'payment3'), 'CASHBACK_RECEIVED')

    @timeout(0.4)
    def test_level_3_case_10_cashback_processed_before_operation(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 100), 100)
        self.assertEqual(self.system.pay(4, 'account1', 100), 'payment1')
        self.assertIsNone(self.system.pay(5, 'account1', 1))
        self.assertIsNone(self.system.transfer(86400003, 'account1', 'account2', 1))
        self.assertEqual(self.system.transfer(86400004, 'account1', 'account2', 2), 0)
        self.assertIsNone(self.system.pay(86400005, 'account1', 1))
        self.assertEqual(
            self.system.top_spenders(86400006, 2),
            ['account1(102)', 'account2(0)']
        )


if __name__ == '__main__':
    unittest.main()
