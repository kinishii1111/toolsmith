# Sessão B — Recall: thread `alice` isolada (não vê a sessão A)

> Requisito: `GROQ_API_KEY` no `.env`. Threads isoladas por `thread_id` — a sessão B usa
> `alice`, **diferente** da sessão A (`kin-nome`), então não herda aquela memória.
> Ouro: thread `kin-nome` e thread `alice` coexistem sem se misturar no `data/checkpoints.sqlite`.

## 1) Thread nova e isolada — pergunta o nome

```bash
python3 -m toolsmith chat --thread alice "Ola! Qual seu nome?"
```

**O que esperar**

- Assim como na sessão A, o agente se apresenta — mas agora no contexto da thread `alice`.
- A conversa da sessão A (`kin-nome`) **não** vaza pra cá: cada `thread_id` tem seu próprio histórico.

## 2) Testar o isolamento — alice não conhece o Kin

```bash
python3 -m toolsmith chat --thread alice "Qual o nome que a thread kin-nome aprendeu?"
```

**O que esperar**

- O agente **não** sabe o nome aprendido na outra thread (`kin-nome`). Confirma que memória é por `thread_id` (memória curta de conversa), não global.

## 3) Isolamento inverso — kin-nome continua intacta

```bash
python3 -m toolsmith chat --thread kin-nome "Qual meu nome mesmo?"
```

**O que esperar**

- A thread `kin-nome` ainda lembra o nome `Kin` — a sessão B (`alice`) não a alterou.

## 4) Inspect das duas threads

```bash
python3 -m toolsmith threads
python3 -m toolsmith inspect kin-nome
python3 -m toolsmith inspect alice
```

**O que esperar**

- `threads` lista as duas (`kin-nome` e `alice`).
- `inspect` mostra checkpoints independentes: `kin-nome` com o nome `Kin`; `alice` com a conversa dela.

---
Ver: `examples/session_a.md` (thread `kin-nome`) · `README.md` (seção Recall/memória).
