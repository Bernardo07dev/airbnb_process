# Level 3 — Payments with Delayed Cashback

## Overview
At Level 3, the banking system should allow processing payments with delayed cashback and checking the status of those payments.

Every successful payment qualifies for a **2% cashback** (rounded down to the nearest integer) that is automatically refunded into the account exactly **24 hours (86,400,000 milliseconds)** after the payment timestamp.

---

## Methods to Implement

### `pay(timestamp: int, account_id: str, amount: int) -> str | None`
Withdraws `amount` from `account_id` and registers a delayed cashback refund.

- **Parameters:**
  - `timestamp`: Integer timestamp in milliseconds.
  - `account_id`: String identifier for the paying account.
  - `amount`: Integer payment amount (amount > 0).
- **Payment ID Convention:**
  - On success, returns a globally unique string: `"payment1"`, `"payment2"`, `"payment3"`, etc.
  - The counter is **global** across all accounts.
  - The counter increments **only upon a successful payment**.
- **Cashback Mechanics:**
  - Cashback amount: `int(amount * 0.02)` (rounded down).
  - Refund timestamp: `timestamp + 86_400_000`.
  - When the cashback due timestamp is reached or passed by any subsequent bank operation, the cashback is credited to the account and the payment status changes to `"CASHBACK_RECEIVED"`.
- **Ranking (`top_spenders`):**
  - The paid `amount` counts towards `account_id`'s total outgoing funds.
  - The received cashback refund does **not** reduce the outgoing funds.
- **Returns:**
  - The generated payment ID (e.g., `"payment1"`).
  - `None` if the account does not exist or has insufficient funds (< `amount`).

---

### `get_payment_status(timestamp: int, account_id: str, payment: str) -> str | None`
Returns the current status of the payment identified by `payment`.

- **Parameters:**
  - `timestamp`: Integer timestamp in milliseconds.
  - `account_id`: String identifier of the account that made the payment.
  - `payment`: String payment identifier (e.g., `"payment1"`).
- **Status Values:**
  - `"IN_PROGRESS"`: Payment was successful, but the 24-hour delay has not yet passed (`current_timestamp < payment_timestamp + 86_400_000`).
  - `"CASHBACK_RECEIVED"`: 24 hours have passed (`current_timestamp >= payment_timestamp + 86_400_000`), and the cashback refund has been processed.
- **Returns:**
  - The status string (`"IN_PROGRESS"` or `"CASHBACK_RECEIVED"`).
  - `None` if:
    - The account does not exist.
    - The payment ID does not exist.
    - The payment does not belong to `account_id`.

---

## Examples

```python
bank = BankingSystem()
bank.create_account(1, "account1")
bank.deposit(2, "account1", 1000)

bank.pay(100, "account1", 500)
# -> "payment1" (cashback = 10; due at 100 + 86400000 = 86400100)

bank.get_payment_status(200, "account1", "payment1")
# -> "IN_PROGRESS"

bank.get_payment_status(86400100, "account1", "payment1")
# -> "CASHBACK_RECEIVED" (account balance is now 500 + 10 = 510)
```
