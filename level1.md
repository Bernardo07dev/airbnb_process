# Level 1 — Accounts, Deposits, and Transfers

## Overview
Your task is to implement a simplified version of a banking system. At Level 1, the banking system should support creating new accounts, depositing money into accounts, and transferring money between two accounts.

All operations have a `timestamp` parameter — a timestamp in milliseconds. All timestamps are unique and in the range `1` to `10^9`. Operations are given in strictly increasing timestamp order.

---

## Methods to Implement

### `create_account(timestamp: int, account_id: str) -> bool`
Creates a new account with the given identifier if it does not already exist.

- **Parameters:**
  - `timestamp`: Integer timestamp in milliseconds.
  - `account_id`: String identifier for the account.
- **Returns:**
  - `True` if the account was successfully created.
  - `False` if an account with `account_id` already exists.

---

### `deposit(timestamp: int, account_id: str, amount: int) -> int | None`
Deposits the specified amount into the account with the given `account_id`.

- **Parameters:**
  - `timestamp`: Integer timestamp in milliseconds.
  - `account_id`: String identifier for the account.
  - `amount`: Integer amount to deposit (amount > 0).
- **Returns:**
  - The balance of the account after the operation.
  - `None` if the account does not exist.

---

### `transfer(timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None`
Transfers the given `amount` from `source_account_id` to `target_account_id`.

- **Parameters:**
  - `timestamp`: Integer timestamp in milliseconds.
  - `source_account_id`: String identifier for the source account.
  - `target_account_id`: String identifier for the target account.
  - `amount`: Integer amount to transfer (amount > 0).
- **Returns:**
  - The balance of the source account after the transfer succeeds.
  - `None` if:
    - `source_account_id == target_account_id`
    - `source_account_id` does not exist
    - `target_account_id` does not exist
    - `source_account_id` has insufficient funds (< `amount`)

---

## Examples

```python
bank = BankingSystem()
bank.create_account(1, "account1")  # -> True
bank.create_account(2, "account1")  # -> False (already exists)
bank.create_account(3, "account2")  # -> True
bank.deposit(4, "account1", 1000)   # -> 1000
bank.deposit(5, "non_existing", 500)# -> None
bank.transfer(6, "account1", "account2", 300) # -> 700
bank.transfer(7, "account1", "account1", 100) # -> None (source == target)
bank.transfer(8, "account1", "account2", 1000) # -> None (insufficient funds)
```
