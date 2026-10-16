import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.timeout_compat import timeout
from banking_system_impl import BankingSystemImpl


class HardcoreEdgeCaseTests(unittest.TestCase):
    """
    Testes avançados simulando os 'hidden test cases' do CodeSignal:
    - Encadeamento de Merges (A <- B <- C)
    - Reembolso de cashback caindo no saldo histórico
    - Recriação múltipla de contas
    - Top spenders após merge sucessivo
    """

    failureException = Exception

    def setUp(self):
        self.system = BankingSystemImpl()

    @timeout(0.4)
    def test_chained_merges(self):
        # A <- B, e depois C <- A
        self.system.create_account(1, "A")
        self.system.create_account(2, "B")
        self.system.create_account(3, "C")

        self.system.deposit(4, "A", 100)
        self.system.deposit(5, "B", 200)
        self.system.deposit(6, "C", 300)

        # B faz um pagamento
        p_b = self.system.pay(10, "B", 100) # cashback 2 vence em 10 + 86400000 = 86400010

        # Merge 1: B entra em A no tempo 20
        self.assertTrue(self.system.merge_accounts(20, "A", "B"))
        # A tem: 100 + 100 (saldo de B pós-pay) = 200

        # Merge 2: A entra em C no tempo 30
        self.assertTrue(self.system.merge_accounts(30, "C", "A"))
        # C tem: 300 + 200 = 500

        # Pagamento que era de B deve responder para C!
        self.assertEqual(self.system.get_payment_status(40, "C", p_b), "IN_PROGRESS")
        self.assertIsNone(self.system.get_payment_status(40, "A", p_b))
        self.assertIsNone(self.system.get_payment_status(40, "B", p_b))

        # Quando o cashback vencer, deve ir para C (saldo vira 500 + 2 = 502)
        self.assertEqual(self.system.get_payment_status(86400010, "C", p_b), "CASHBACK_RECEIVED")
        self.assertEqual(self.system.deposit(86400011, "C", 0), 502)

    @timeout(0.4)
    def test_historical_balance_with_cashback(self):
        self.system.create_account(1, "alice")
        self.system.deposit(2, "alice", 1000)

        # Pagamento de 500 no tempo 100 -> saldo fica 500
        # Cashback de 10 cai exatamente no tempo 86400100
        self.system.pay(100, "alice", 500)

        # Consulta no tempo 90000000 (muito depois do cashback cair)
        # 1. Antes do cashback cair (tempo 500) -> deve ser 500
        self.assertEqual(self.system.get_balance(90000000, "alice", 500), 500)
        # 2. No exato instante do cashback (tempo 86400100) -> deve ser 510
        self.assertEqual(self.system.get_balance(90000000, "alice", 86400100), 510)

    @timeout(0.4)
    def test_top_spenders_after_merges(self):
        self.system.create_account(1, "user1")
        self.system.create_account(2, "user2")
        self.system.create_account(3, "user3")

        self.system.deposit(4, "user1", 1000)
        self.system.deposit(5, "user2", 1000)
        self.system.deposit(6, "user3", 1000)

        self.system.transfer(7, "user1", "user2", 200) # user1 outgoing: 200
        self.system.transfer(8, "user2", "user3", 300) # user2 outgoing: 300

        # user2 entra em user3. user3 herda os 300 de outgoing de user2!
        self.system.merge_accounts(9, "user3", "user2")

        # user3 tinha 0, agora tem 300. user1 tem 200. user2 não existe mais.
        self.assertEqual(
            self.system.top_spenders(10, 5),
            ["user3(300)", "user1(200)"]
        )

    @timeout(0.4)
    def test_multiple_account_recreations_and_isolated_histories(self):
        # 1ª encarnação de X: vive de 1 a 10
        self.system.create_account(1, "X")
        self.system.create_account(2, "Y")
        self.system.deposit(3, "X", 100)
        self.system.merge_accounts(10, "Y", "X")

        # 2ª encarnação de X: vive de 20 a 30
        self.system.create_account(20, "X")
        self.system.deposit(25, "X", 500)
        self.system.merge_accounts(30, "Y", "X")

        # 3ª encarnação de X: criada no tempo 40 e viva
        self.system.create_account(40, "X")
        self.system.deposit(45, "X", 999)

        # Consultas históricas em tempo 50:
        self.assertEqual(self.system.get_balance(50, "X", 5), 100)  # 1ª vida
        self.assertIsNone(self.system.get_balance(50, "X", 15))      # limbo 1
        self.assertEqual(self.system.get_balance(50, "X", 26), 500)  # 2ª vida
        self.assertIsNone(self.system.get_balance(50, "X", 35))      # limbo 2
        self.assertEqual(self.system.get_balance(50, "X", 46), 999)  # 3ª vida


if __name__ == "__main__":
    unittest.main()
