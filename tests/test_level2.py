import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class Level2Tests(unittest.TestCase):
    """
    CodeSignal Level 2 Test Suite:
    - Ranking accounts based on outgoing transactions (`top_spenders`)
    - Primary sort: descending outgoing amount
    - Tie-breaker: ascending alphabetical account_id
    """

    failureException = Exception

    def setUp(self):
        self.system = BankingSystemImpl()

    @timeout(0.4)
    def test_top_spenders_ranking_and_ties(self):
        self.system.create_account(1, "alice")
        self.system.create_account(2, "bob")
        self.system.create_account(3, "charlie")

        self.system.deposit(4, "alice", 1000)
        self.system.deposit(5, "bob", 1000)
        self.system.deposit(6, "charlie", 1000)

        # Before any spending: all 0, tie-breaker alphabetical
        self.assertEqual(
            self.system.top_spenders(7, 3),
            ["alice(0)", "bob(0)", "charlie(0)"]
        )

        # Transfers out generate outgoing
        self.system.transfer(8, "charlie", "bob", 300)
        self.system.transfer(9, "alice", "bob", 500)

        # alice=500, charlie=300, bob=0 (received funds do not count as outgoing)
        self.assertEqual(
            self.system.top_spenders(10, 2),
            ["alice(500)", "charlie(300)"]
        )
        self.assertEqual(
            self.system.top_spenders(11, 5),
            ["alice(500)", "charlie(300)", "bob(0)"]
        )

    @timeout(0.4)
    def test_top_spenders_tie_breaker_alphabetical(self):
        self.system.create_account(1, "zack")
        self.system.create_account(2, "adam")
        self.system.create_account(3, "ben")

        self.system.deposit(4, "zack", 500)
        self.system.deposit(5, "adam", 500)
        self.system.deposit(6, "ben", 500)

        self.system.transfer(7, "zack", "ben", 100)
        self.system.transfer(8, "adam", "ben", 100)

        # adam and zack tied at 100, adam comes first; ben at 0
        self.assertEqual(
            self.system.top_spenders(9, 2),
            ["adam(100)", "zack(100)"]
        )


if __name__ == "__main__":
    unittest.main()
