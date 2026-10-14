# Level 4 — Handoff de Progresso e Metodologia

> Documento de contexto para outra IA assumir a tutoria do Level 4 do desafio
> CodeSignal "Banking System". Resume o que já foi implementado, as decisões de
> design e o que ainda falta. **Não é uma solução pronta** — o aluno está
> implementando sozinho sob tutoria.

---

## Metodologia em uso (ler antes de interagir)

O aluno está sendo guiado como tutor, não recebendo a solução pronta. Regras
que vêm do `AGENTS.md` do projeto e que devem ser mantidas:

- **Guiar, não entregar.** Nunca colar a classe completa nem resolver um método
  inteiro de uma vez. Dar o menor hint que destrava.
- **Um passo de cada vez.** Um método (ou um bug) por rodada. Pedir pro aluno
  escrever/alterar e mostrar antes de avançar.
- **Ser terso.** Liderar pela conclusão, sem preâmbulo nem recapitulação. Uma
  pergunta ou um próximo passo concreto por vez. Expandir só quando o aluno
  pede detalhe ou quando correção/debug exige.
- **Responder em pt-br** (o aluno pediu; o default do AGENTS.md era inglês).
- **Fonte de verdade** é o enunciado oficial (reproduzido no `AGENTS.md`). O
  arquivo `banking_system_impl.txt` é referência que passou nos testes, mas
  **não** deve ser colado pro aluno.
- Preservar nomes/assinaturas/retornos oficiais dos métodos.
- Revisar o código que o aluno **realmente escreveu**; apontar o **primeiro**
  problema concreto, não reescrever tudo.

Fluxo típico por método: interpretar requisito → decidir entrada/saída e casos →
decidir dados a guardar → hint → aluno implementa → revisão (1º bug) → testar.

---

## Decisão de arquitetura central do Level 4

O Level 4 obriga a **separar duas coisas que antes eram a mesma**:

- **Nome da conta** (`account_id`, string): é reutilizável. Depois de um merge
  remover o nome, `create_account` pode recriá-lo como conta nova e
  independente.
- **Instância da conta** (um ciclo de vida): uma criação → no máximo uma
  remoção por merge. Seu saldo, histórico e janela `[created, removed)` têm que
  sobreviver pra sempre, mesmo depois do nome sumir ou ser recriado.

Implementação dessa separação no `Bank`:

```python
self.instances = {}   # inst_id (int)      -> Account   (registro permanente, inclui mortas)
self.active    = {}   # account_id (str)   -> inst_id   (só contas vivas; é o lookup por nome)
self.inst_count = 0   # gera inst_id único; incrementa a cada create_account
```

- `self.instances` é indexado por `inst_id` (não pelo nome!), pra que um nome
  recriado **não** sobrescreva a instância antiga.
- `self.active` mapeia o nome vivo pro `inst_id`. Merge remove o nome daqui;
  recriação sobrescreve com nova instância.

### Helper de resolução por nome

```python
def acc(self, account_id):
    active = self.active.get(account_id)
    if not active:            # nome não existe/não está vivo (inst_id começa em 1, nunca 0)
        return active         # None
    return self.instances[active]
```

Todos os métodos L1-L3 passaram a resolver a conta via `self.acc(nome)` em vez
de `self.instances[nome]`.

---

## Classe `Account` (account.py)

```python
class Account():
    def __init__(self, account_id, instance_id, created, removed=None):
        self.account_id = account_id
        self.instance_id = instance_id
        self.balance = 0
        self.outgoing = 0
        self.created = created          # timestamp de criação (início da janela de vida)
        self.removed = removed          # timestamp do merge que removeu; None enquanto viva
        self.history = [(created, 0)]   # lista (timestamp, balance), ordem crescente de tempo
```

- `history` guarda o **saldo depois** de cada mudança (não o delta).
- Default mutável (`history=[]`) foi evitado de propósito — a lista é criada
  dentro do `__init__`.

---

## Estado atual dos métodos (bank.py)

Todos chamam `self.cashback_desc(timestamp)` no início (processa cashbacks com
`due <= timestamp` antes de qualquer coisa).

- **create_account**: falha (`False`) se `self.acc(nome)` já existe. Senão
  incrementa `inst_count`, cria `Account(nome, inst_count, timestamp)`, grava em
  `self.instances[inst_count]` e `self.active[nome] = inst_count`.
- **deposit / transfer / pay**: resolvem via `self.acc(...)`, validam antes de
  mutar, e dão `history.append((timestamp, acc.balance))` a cada mudança de
  saldo (no transfer, nos dois lados).
- **top_spenders**: itera só contas **vivas** —
  `[self.instances[i] for i in self.active.values()]` — pra não contar
  instâncias mortas por merge nem duplicar outgoing.
- **get_payment_status**: resolve via `self.acc(...)`; valida pagamento
  existente e `payment.account_id == account_id`.
- **cashback_desc**: FIFO (`deque`). Para cada cashback vencido: marca status
  `CASHBACK_RECEIVED`, resolve a conta pelo nome, credita o saldo e grava
  `history.append((cashback.due, acc.balance))` — **no due time**, não no
  timestamp atual. O `popleft()` é **incondicional** (fora do `if acc:`) pra não
  entrar em loop infinito quando a conta não for encontrada.

### merge_accounts (implementado)

Merge de `account_id_2` **em** `account_id_1`:

1. `cashback_desc(timestamp)`.
2. `False` se `id1 == id2`.
3. Resolve ambos via `self.acc`; `False` se qualquer um não existir.
4. Reescreve posse dos **cashbacks** pendentes de `id2` → `id1` (refund futuro
   cai no ativo).
5. Reescreve posse dos **payments** de `id2` → `id1` (iterando
   `self.payments.values()`) pra `get_payment_status(id1, pagamento_do_id2)`
   funcionar.
6. `self.active.pop(id2)` (tira o nome do vivo; **não** apaga de `instances`).
7. `acc1.balance += acc2.balance` e `history.append((timestamp, acc1.balance))`.
8. `acc1.outgoing += acc2.outgoing`.
9. `acc2.removed = timestamp` (fecha a janela de vida).
10. `return True`.

`Payment` e `Cashback` guardam o **nome** do dono (string), por isso o merge
reescreve esse nome. A abordagem é "reescrever posse" (não mapa de alias), o que
evita a armadilha do id recriado: cadeias (`A<-B`, depois `C<-A`) funcionam
porque cada merge reescreve de novo.

---

## O que ainda FALTA

### get_balance(self, timestamp, account_id, time_at) -> int | None (não implementado)

Retorna o saldo de `account_id` em `time_at`, ou `None` se a conta não existia
naquele instante.

Decisões/pontos ainda a trabalhar com o aluno (via hints, sem entregar):

- **Qual instância usar.** `self.acc` não serve: conta mergeada já saiu de
  `active` mas ainda tem que responder. Precisa achar a instância pela janela de
  vida. (Possível ponto de design pendente: como localizar a instância certa de
  um nome que pode ter tido várias encarnações — ex.: guardar por nome a lista
  de instâncias já criadas, ou varrer `self.instances`.)
- **Janela de existência:** `None` se `time_at < created` ou
  (`removed is not None and time_at >= removed`). Caso contrário responde.
- **Busca no history:** achar o último registro com `ts <= time_at`. Como o
  history está ordenado por tempo, usar **busca binária** (`bisect`) em vez de
  varredura linear. Sugerir `bisect` da stdlib.
- **Edge cases:** vários eventos no mesmo timestamp — a query tem que ver o
  valor final (o último append daquele ts). Cashback entra no history no **due
  time**, que pode ser anterior ao timestamp que disparou o processamento.

---

## Arquivos

- `bank.py` — classe `Bank` (lógica principal).
- `account.py` — classe `Account`.
- `payments.py` — classe `Payment` (guarda nome do dono, id, amount, timestamp, status).
- `cashback.py` — classe `Cashback` (nome do dono, payment_id, cash_value, due).
- `main.py` — testes manuais do aluno.
- `banking_system_impl.txt` — referência que passou nos testes (NÃO mostrar ao aluno).
- `AGENTS.md` — regras de tutoria + enunciado oficial completo.

Status: L1-L3 rodando; `merge_accounts` implementado; `get_balance` pendente.
