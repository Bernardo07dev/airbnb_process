# Level 3 - Payments with Delayed Cashback

## Methods

```python
pay(self, timestamp: int, account_id: str, amount: int) -> str | None
```

- Returns a payment id string: `"payment1"`, `"payment2"`, ... (global counter).
- Returns `None` if the account does not exist or has insufficient funds.

```python
get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None
```

- Returns `"IN_PROGRESS"` or `"CASHBACK_RECEIVED"`.
- Returns `None` if the account does not exist, the payment does not exist, or the payment belongs to a different account.

## Key rules

`pay` withdraws `amount` and earns 2% cashback, rounded down, refunded 24h later.

Cashback delay: `86400000` ms. Processed at `timestamp + 86400000`.

Cashback must be applied before any other transaction at that timestamp.

Payment counter increments only on successful withdrawals

`pay` withdrawals count toward `top_spenders` outgoing.

Cashback increases balance but never changes outgoing.
