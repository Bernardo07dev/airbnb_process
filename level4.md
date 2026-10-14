# Level 4 - Merging Accounts and Balance History

## Methods

```python
merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool
```

Merges `account_id_2` into `account_id_1`. Returns `True` on success, `False` otherwise.

- Returns `False` if `account_id_1 == account_id_2`.
- Returns `False` if either account does not exist.

```python
get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None
```

Returns the balance of `account_id` at `time_at`. Returns `None` if the account did not exist at `time_at`.

## merge rules

- `account_id_2`'s balance is added to `account_id_1`.
- Pending cashbacks for `account_id_2` must still be processed, but refunded to `account_id_1`.
- After the merge, `get_payment_status` for `account_id_2`'s payments must work when called with `account_id_1`.
- `top_spenders` outgoing = sum of money transferred/withdrawn by both accounts.
- `account_id_2` is removed from the system after the merge.

## get_balance rules

- Existence is judged by the account's own history window: from `create_account` up to the `merge_accounts` that removed it (if any), not whether it is present now.
- A merged-away account must still answer for any `time_at` in `[created, removed)`. Only `time_at < created` or `time_at >= removed` returns `None`.
- If operations ran at `time_at`, the balance reflects the state after those operations.
- A merged account inherits the balance history of the account merged into it.
- An id recreated via `create_account` after a merge starts a fresh, independent history.

## edge cases to watch

- Multiple balance changes at the same timestamp (e.g. cashback + deposit): the query must see the final value.
- Cashback is recorded at its due time, which may be earlier than the operation that triggered processing.
- Chained merges (`A <- B`, then `C <- A`): payment ownership and pending cashbacks must redirect through the chain.
- Separate "account id" (reusable name) from "account instance/lifetime" (one creation -> one removal).
