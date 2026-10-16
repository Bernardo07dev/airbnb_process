# CHECK - errinhos comuns por level

## Geral
- Todo método público começa com `check_cashbacks(timestamp)`.
- Se o teste de leitura falha, o bug está em quem escreveu o dado.

## Level 1
- `create_account` em conta existente retorna `False`.
- `transfer` para a mesma conta retorna `None`.
- Checar as duas contas com `not (a and b)`, nunca `not (a, b)`.
- Saldo insuficiente é `balance < amount` (saldo igual ao valor pode).
- Toda mudança de saldo grava no `history`, inclusive na conta destino.

## Level 2
- Ordenação `(-outgoing, account_id)`.
- Só contas ativas entram no ranking.
- Transferência que falhou não soma em `outgoing`.
- Depósito e cashback nunca somam em `outgoing`.
- Retornar `[:n]`, mesmo quando `n` é maior que o número de contas.

## Level 3
- O contador de payment só incrementa quando o pagamento dá certo.
- Cashback é `amount * 2 // 100`.
- O vencimento é `timestamp + 86400000`, com `<=` no `check_cashbacks`.
- O cashback é aplicado antes da operação no mesmo timestamp.
- `get_payment_status` usa `get_acc(account_id)`, não a string crua.
- Payment de outra conta retorna `None`.

## Level 4
- `merge_accounts` grava `merged.removed = timestamp`, não basta tirar de `actives`.
- No merge, somar `balance` e `outgoing` na conta que fica.
- Redirecionar `account_id` em todos os cashbacks pendentes e em todos os payments.
- Gravar no `history` da conta que fica, com o saldo somado, no timestamp do merge.
- O histórico do cashback usa `due`, nunca o `timestamp` da operação que o processou.
- A janela de existência é `created <= time_at < removed`.
- `time_at == removed` retorna `None`.
- Conta recriada é uma instância nova, com histórico do zero.
- `get_balance` busca a instância pelo `account_id` em todas as instâncias, inclusive removidas.
- No merge em cadeia (B -> A, depois A -> C), os payments de B precisam aparecer em C.
