import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class Level2Tests(unittest.TestCase):
    """
    The test class below includes 10 tests for Level 2.

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
    def test_level_2_case_01_basic_top_spenders(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertTrue(self.system.create_account(3, 'account3'))
        self.assertEqual(
            self.system.top_spenders(4, 3),
            ['account1(0)', 'account2(0)', 'account3(0)']
        )
        self.assertEqual(self.system.top_spenders(5, 1), ['account1(0)'])

    @timeout(0.4)
    def test_level_2_case_02_top_spenders_after_transfers(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertTrue(self.system.create_account(3, 'account3'))
        self.assertEqual(self.system.deposit(4, 'account1', 1000), 1000)
        self.assertEqual(self.system.deposit(5, 'account2', 1000), 1000)
        self.assertEqual(self.system.deposit(6, 'account3', 1000), 1000)
        self.assertEqual(self.system.transfer(7, 'account1', 'account2', 300), 700)
        self.assertEqual(self.system.transfer(8, 'account3', 'account1', 500), 500)
        self.assertEqual(self.system.transfer(9, 'account2', 'account1', 100), 1200)
        self.assertEqual(
            self.system.top_spenders(10, 3),
            ['account3(500)', 'account1(300)', 'account2(100)']
        )
        self.assertEqual(
            self.system.top_spenders(11, 2),
            ['account3(500)', 'account1(300)']
        )

    @timeout(0.4)
    def test_level_2_case_03_ties_sorted_alphabetically(self):
        self.assertTrue(self.system.create_account(1, 'zeta'))
        self.assertTrue(self.system.create_account(2, 'alpha'))
        self.assertTrue(self.system.create_account(3, 'mike'))
        self.assertTrue(self.system.create_account(4, 'beta'))
        self.assertEqual(self.system.deposit(5, 'zeta', 1000), 1000)
        self.assertEqual(self.system.deposit(6, 'alpha', 1000), 1000)
        self.assertEqual(self.system.deposit(7, 'mike', 1000), 1000)
        self.assertEqual(self.system.deposit(8, 'beta', 1000), 1000)
        self.assertEqual(self.system.transfer(9, 'zeta', 'alpha', 200), 800)
        self.assertEqual(self.system.transfer(10, 'mike', 'alpha', 200), 800)
        self.assertEqual(self.system.transfer(11, 'beta', 'alpha', 50), 950)
        self.assertEqual(
            self.system.top_spenders(12, 4),
            ['mike(200)', 'zeta(200)', 'beta(50)', 'alpha(0)']
        )
        self.assertEqual(
            self.system.top_spenders(13, 2),
            ['mike(200)', 'zeta(200)']
        )

    @timeout(0.4)
    def test_level_2_case_04_n_greater_than_number_of_accounts(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account2', 100), 100)
        self.assertEqual(self.system.transfer(4, 'account2', 'account1', 40), 60)
        self.assertEqual(
            self.system.top_spenders(5, 10),
            ['account2(40)', 'account1(0)']
        )

    @timeout(0.4)
    def test_level_2_case_05_no_accounts(self):
        self.assertEqual(self.system.top_spenders(1, 5), [])
        self.assertTrue(self.system.create_account(2, 'account1'))
        self.assertEqual(self.system.top_spenders(3, 5), ['account1(0)'])

    @timeout(0.4)
    def test_level_2_case_06_failed_transfers_not_counted(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 100), 100)
        self.assertIsNone(self.system.transfer(4, 'account1', 'account2', 500))
        self.assertIsNone(self.system.transfer(5, 'account1', 'account1', 50))
        self.assertIsNone(self.system.transfer(6, 'account2', 'account1', 10))
        self.assertIsNone(self.system.transfer(7, 'account1', 'account3', 10))
        self.assertEqual(
            self.system.top_spenders(8, 2),
            ['account1(0)', 'account2(0)']
        )
        self.assertEqual(self.system.transfer(9, 'account1', 'account2', 100), 0)
        self.assertEqual(
            self.system.top_spenders(10, 2),
            ['account1(100)', 'account2(0)']
        )

    @timeout(0.4)
    def test_level_2_case_07_deposits_not_counted(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 10000), 10000)
        self.assertEqual(self.system.deposit(4, 'account2', 5), 5)
        self.assertEqual(self.system.transfer(5, 'account2', 'account1', 5), 0)
        self.assertEqual(
            self.system.top_spenders(6, 2),
            ['account2(5)', 'account1(0)']
        )
        self.assertEqual(self.system.deposit(7, 'account1', 99999), 110004)
        self.assertEqual(self.system.top_spenders(8, 1), ['account2(5)'])

    @timeout(0.4)
    def test_level_2_case_08_outgoing_accumulates(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 1000), 1000)
        self.assertEqual(self.system.transfer(4, 'account1', 'account2', 100), 900)
        self.assertEqual(self.system.transfer(5, 'account2', 'account1', 100), 0)
        self.assertEqual(self.system.transfer(6, 'account1', 'account2', 250), 750)
        self.assertEqual(self.system.transfer(7, 'account2', 'account1', 250), 0)
        self.assertEqual(self.system.transfer(8, 'account1', 'account2', 1), 999)
        self.assertEqual(
            self.system.top_spenders(9, 2),
            ['account1(351)', 'account2(350)']
        )
        self.assertEqual(self.system.transfer(10, 'account2', 'account1', 1), 0)
        self.assertEqual(
            self.system.top_spenders(11, 2),
            ['account1(351)', 'account2(351)']
        )

    @timeout(0.4)
    def test_level_2_case_09_ranking_changes_over_time(self):
        self.assertTrue(self.system.create_account(1, 'acc_a'))
        self.assertTrue(self.system.create_account(2, 'acc_b'))
        self.assertTrue(self.system.create_account(3, 'acc_c'))
        self.assertEqual(self.system.deposit(4, 'acc_a', 1000), 1000)
        self.assertEqual(self.system.deposit(5, 'acc_b', 1000), 1000)
        self.assertEqual(self.system.deposit(6, 'acc_c', 1000), 1000)
        self.assertEqual(self.system.transfer(7, 'acc_c', 'acc_a', 100), 900)
        self.assertEqual(self.system.top_spenders(8, 1), ['acc_c(100)'])
        self.assertEqual(self.system.transfer(9, 'acc_b', 'acc_a', 150), 850)
        self.assertEqual(self.system.top_spenders(10, 1), ['acc_b(150)'])
        self.assertEqual(self.system.transfer(11, 'acc_a', 'acc_b', 1250), 0)
        self.assertEqual(
            self.system.top_spenders(12, 3),
            ['acc_a(1250)', 'acc_b(150)', 'acc_c(100)']
        )
        self.assertEqual(self.system.transfer(13, 'acc_c', 'acc_b', 900), 0)
        self.assertEqual(
            self.system.top_spenders(14, 3),
            ['acc_a(1250)', 'acc_c(1000)', 'acc_b(150)']
        )

    @timeout(0.4)
    def test_level_2_case_10_lexicographic_tie_break(self):
        self.assertTrue(self.system.create_account(1, 'account10'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertTrue(self.system.create_account(3, 'account1'))
        self.assertEqual(
            self.system.top_spenders(4, 3),
            ['account1(0)', 'account10(0)', 'account2(0)']
        )
        self.assertTrue(self.system.create_account(5, 'Zed'))
        self.assertEqual(
            self.system.top_spenders(6, 4),
            ['Zed(0)', 'account1(0)', 'account10(0)', 'account2(0)']
        )


if __name__ == '__main__':
    unittest.main()
