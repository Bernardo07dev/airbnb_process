# AGENTS.md — Banking System Practice: Solo Challenge Mode

## Language & Tone

- **All responses must be in English**, unless explicitly instructed otherwise by the student.
- **Be terse and prompt-focused.** Lead with the point. No preambles, no unsolicited code, no solutions.

---

## Current Mode: Solo Practice (Prompt-Only AI)

The student is preparing for the real assessment and will now **code completely from scratch on their own without AI assistance or hints**.

### AI Role:
- **Strictly an examiner / test orchestrator**: Present the problem statement, requirements, and test cases level by level.
- **No code hints, no debugging help, no solution delivery**: Do NOT point out syntax errors, edge cases, or logic flaws unless the student explicitly asks to switch back to tutor mode.
- **Give only test feedback**: When the student runs tests, report test results or prompt for the next level once the current one passes.

---

## Strategy & Architectural Decisions (Learned from Iteration)

This section documents the verified architecture and algorithmic decisions developed to solve Levels 1–4 cleanly and pass all performance and edge-case requirements:

### 1. Domain Modeling & Separation of Concerns
Instead of monolithic nested dictionaries, divide the system into dedicated domain entities:
- **`Account`**:
  - `account_id` (str): Account identifier string.
  - `instance_id` (int): Unique lifecycle ID.
  - `balance` (int): Current available balance.
  - `outgoing` (int): Total outgoing funds (transfers out + payments).
  - `created` (int): Creation timestamp.
  - `removed` (int | None): Merge/removal timestamp.
  - `history` (list[tuple[int, int]]): `[(timestamp, balance_after), ...]`.
- **`Payment`**:
  - `account_id`, `payment_id`, `value`, `cashback_id`, `status` (`"IN_PROGRESS"` / `"CASHBACK_RECEIVED"`).
- **`Cashback`**:
  - `account_id`, `payment_id`, `cash_value`, `due` (`timestamp + 86_400_000`).

### 2. Level 4 Key Insight: Account ID vs. Account Instance
- **Problem**: When `account_id_2` is merged into `account_id_1`, `account_id_2` is deleted. However:
  1. The historical balance of `account_id_2` must remain queryable via `get_balance` for any timestamp prior to the merge.
  2. The identifier `account_id_2` can be subsequently recreated via `create_account`, starting a brand new, independent lifecycle.
- **Solution**:
  - `self.instances = {inst_id: Account}`: Permanent storage of all account lifecycles (both living and removed). Never gets deleted.
  - `self.active = {account_id: inst_id}`: Maps living account names to their current active `inst_id`. Merging deletes from `self.active`; creating writes to `self.active`.
  - Lookup helper `acc(account_id)` resolves through `self.active`.

### 3. Timestamp Ordering & Eager Cashback Processing
- Timestamps arrive in strictly increasing order.
- Delayed cashback queue: `self.cashbacks = deque()`.
- Every public bank method starts by processing all pending cashbacks with `due <= timestamp`:
  ```python
  while self.cashbacks and self.cashbacks[0].due <= timestamp:
      cb = self.cashbacks.popleft()
      # apply refund and record history at cb.due
  ```
- Because delay is constant (24h = `86_400_000` ms) and operations arrive in increasing timestamp order, elements in the deque are naturally ordered by `due`. Processing is $O(1)$ amortized per item.

### 4. Ranking (`top_spenders`)
- Outgoing accumulates on withdrawals (`pay`) and outgoing transfers (`transfer`), never on deposits or cashbacks.
- Multi-key sorting: descending outgoing, then ascending alphabetical `account_id`:
  ```python
  sorted(valid_accounts, key=lambda a: (-a.outgoing, a.account_id))[:n]
  ```

### 5. Historical Balance (`get_balance`)
- Must match the correct instance window: `inst.created <= time_at and (inst.removed is None or time_at < inst.removed)`.
- Returns `None` if outside existence window.
- Returns `0` if account existed but had no transactions `<= time_at`.
- Returns the latest balance record with `ts <= time_at`.
- *Performance note*: For production scale, search in `acc.history` using binary search (`bisect`) instead of linear scan.

---

## Official Specification

### General Requirements

> Your task is to implement a simplified version of a banking system. Plan your design according to the level specifications below:
>
> - **Level 1:** Account creation, deposits, and transfers between 2 accounts.
> - **Level 2:** Ranking accounts based on outgoing transactions (`top_spenders`).
> - **Level 3:** Processing payments with delayed cashback (24h = 86,400,000 ms) and payment status.
> - **Level 4:** Merging accounts and historical balance queries (`get_balance`).

**Global constraints:**
- Operations arrive in strictly increasing `timestamp` order.
- Timestamps are unique integers in milliseconds (`1` to `10^9`).

---

### Level 1 — Accounts, Deposits, Transfers

| Method | Behavior | Returns |
| :--- | :--- | :--- |
| `create_account(timestamp: int, account_id: str) -> bool` | Create account if it doesn't exist. | `True` if created; `False` if `account_id` already exists. |
| `deposit(timestamp: int, account_id: str, amount: int) -> int \| None` | Deposit into account. | Balance after operation; `None` if account doesn't exist. |
| `transfer(timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int \| None` | Transfer funds. | Balance of source on success; `None` on failure. |

---

### Level 2 — `top_spenders`

`top_spenders(timestamp: int, n: int) -> list[str]`
- Top `n` accounts with highest total outgoing funds (transferred out or paid).
- Sorted by: `-outgoing`, then `account_id` ascending.
- Format: `["<account_id>(<total_outgoing>)", ...]`.

---

### Level 3 — Payments with Delayed Cashback

`pay(timestamp: int, account_id: str, amount: int) -> str | None`
- Withdraws `amount`, earns 2% cashback (rounded down, `int(amount * 0.02)`), refunded after `86_400_000` ms.
- Returns unique global ID: `"payment1"`, `"payment2"`, etc. Only increments counter on success.
- Returns `None` if account doesn't exist or insufficient funds.

`get_payment_status(timestamp: int, account_id: str, payment: str) -> str | None`
- Returns `None` if account doesn't exist or payment doesn't belong to account.
- Returns `"IN_PROGRESS"` or `"CASHBACK_RECEIVED"`.

---

### Level 4 — Merging Accounts and Balance History

`merge_accounts(timestamp: int, account_id_1: str, account_id_2: str) -> bool`
- Merges `account_id_2` into `account_id_1`. `account_id_2` is removed from active accounts.
- Balance and outgoing of `account_id_2` are added to `account_id_1`.
- Pending cashbacks and payment lookups of `account_id_2` redirect to `account_id_1`.
- Returns `False` if `account_id_1 == account_id_2` or either does not exist.

`get_balance(timestamp: int, account_id: str, time_at: int) -> int | None`
- Returns total balance of `account_id` at `time_at`.
- Returns `None` if account did not exist at `time_at` (`time_at < created` or `time_at >= removed`).
- Reflects state after all operations at `time_at`.
