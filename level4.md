# Level 4 — Merging Accounts and Balance History

## Overview
At Level 4, the banking system should support merging two accounts into one while preserving full balance and transaction histories. The system must also allow historical balance queries across any timestamp.

---

## Methods to Implement

### `merge_accounts(timestamp: int, account_id_1: str, account_id_2: str) -> bool`
Merges `account_id_2` into `account_id_1`.

- **Parameters:**
  - `timestamp`: Integer timestamp in milliseconds.
  - `account_id_1`: String identifier of the target account (retained).
  - `account_id_2`: String identifier of the source account (removed).
- **Rules of Merge:**
  1. `account_id_2` is removed from active accounts.
  2. The current available balance of `account_id_2` is added to `account_id_1`.
  3. The total outgoing funds of `account_id_2` are added to `account_id_1` for future `top_spenders` queries.
  4. Any pending cashbacks originally scheduled for `account_id_2` must now be refunded to `account_id_1`.
  5. Any previous payments made by `account_id_2` must now be queryable via `get_payment_status` using `account_id_1`.
  6. Chained merges (e.g., `B` merged into `A`, then `A` merged into `C`) must forward all ownership and pending cashbacks down the chain to the active account.
- **Returns:**
  - `True` if the merge succeeded.
  - `False` if:
    - `account_id_1 == account_id_2`
    - `account_id_1` does not exist in active accounts
    - `account_id_2` does not exist in active accounts

---

### `get_balance(timestamp: int, account_id: str, time_at: int) -> int | None`
Returns the historical total balance of `account_id` at a specific timestamp `time_at`.

- **Parameters:**
  - `timestamp`: Integer timestamp when the query is executed.
  - `account_id`: String identifier for the account.
  - `time_at`: Integer timestamp for which the balance is requested (`time_at <= timestamp`).
- **Existence Window Rules:**
  - An account's existence is bounded by its specific lifecycle instance: `[created, removed)`.
  - If `time_at < created` or (`removed is not None` and `time_at >= removed`), return `None`.
  - An account that was merged away **must still respond** for any query timestamp where `created <= time_at < removed`.
  - If `account_id` is subsequently recreated via `create_account` after being merged, the new account starts a fresh, independent lifecycle and history.
- **Balance Value Rules:**
  - If the account existed at `time_at` but had no transactions on or before `time_at`, its balance is `0`.
  - If one or more operations occurred exactly at `time_at`, the returned balance reflects the state **after** all operations executed at `time_at`.
  - Cashbacks must be reflected at their **due timestamp** (`payment_timestamp + 86_400_000`).
- **Returns:**
  - The historical balance integer.
  - `None` if the account did not exist at `time_at`.

---

## Examples

```python
bank = BankingSystem()
bank.create_account(1, "account1")
bank.deposit(2, "account1", 1000)
bank.create_account(3, "account2")
bank.deposit(4, "account2", 500)

bank.get_balance(10, "account1", 0)  # -> None (created at 1)
bank.get_balance(10, "account1", 1)  # -> 0
bank.get_balance(10, "account1", 2)  # -> 1000

bank.merge_accounts(20, "account1", "account2") # -> True
bank.get_balance(25, "account2", 4)  # -> 500 (account2 existed at 4)
bank.get_balance(25, "account2", 20) # -> None (account2 removed at 20)
bank.get_balance(25, "account1", 20) # -> 1500 (1000 + 500 merged)
```
