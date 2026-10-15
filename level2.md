# Level 2 — Ranking Accounts by Outgoing Transactions

## Overview
At Level 2, the banking system should support ranking accounts based on their total outgoing transactions.

Outgoing transactions include:
- Successful fund transfers (`transfer`) out of the account.
- Any future withdrawal operations (such as payments introduced in later levels).

Deposits and refunds/cashbacks do **not** contribute to outgoing transactions.

---

## Methods to Implement

### `top_spenders(timestamp: int, n: int) -> list[str]`
Returns the identifiers of the top `n` accounts with the highest outgoing transactions.

- **Parameters:**
  - `timestamp`: Integer timestamp in milliseconds.
  - `n`: Positive integer representing the maximum number of accounts to return.
- **Sorting Criteria:**
  1. Primary: Highest total outgoing funds in **descending order**.
  2. Tie-breaker: If two accounts have the same total outgoing funds, sort alphabetically by `account_id` in **ascending order** (lexicographical order).
- **Format of Output Elements:**
  - Each item in the returned list must be formatted as: `"<account_id>(<total_outgoing_amount>)"`.
  - Example: `["account1(500)", "account2(300)"]`.
- **Edge Cases:**
  - If `n` is greater than the total number of existing accounts, return all existing accounts in ranked order.
  - Accounts with `0` outgoing transactions must still be included if there are fewer than `n` accounts with positive outgoing transactions.

---

## Examples

```python
bank = BankingSystem()
bank.create_account(1, "account1")
bank.create_account(2, "account2")
bank.create_account(3, "account3")
bank.deposit(4, "account1", 1000)
bank.deposit(5, "account2", 1000)
bank.transfer(6, "account1", "account2", 200) # account1 outgoing: 200
bank.transfer(7, "account2", "account3", 500) # account2 outgoing: 500

bank.top_spenders(8, 2)
# -> ["account2(500)", "account1(200)"]

bank.top_spenders(9, 3)
# -> ["account2(500)", "account1(200)", "account3(0)"]
```
