# Sessão A — Recall: thread `kin-nome` (o agente se apresenta e guarda seu nome)

> Requisito: `GROQ_API_KEY` no `.env` (ver README). Sem key o CLI sai com erro (`exit != 0`).
> O checkpoint (memória) vai para `data/checkpoints.sqlite` (SqliteSaver). Threads isoladas por `thread_id`.

## 1) Primeiro contato — pergunta "qual seu nome?"

```bash
python3 -m toolsmith chat --thread kin-nome "Ola! Qual seu nome?"
# --motor scratch|prebuilt (memória por thread em ambos; nó summarize só no scratch)
```

**O que esperar**

- `agent` responde apresentando o Plantão e perguntando o nome do usuário (SystemPrompt por cenário).
- O checkpoint da thread `kin-nome` é salvo no sqlite (cada passo).

## 2) Restart do agente — pergunta o nome de novo

```bash
python3 -m toolsmith chat --thread kin-nome "Restart! Qual meu nome?"
```

**O que esperar**

- Nova instância/processo, **mesma thread** → o agente continua a conversa e já sabe o contexto anterior (pergunta o nome de novo só porque você pediu; a memória da conversa foi restaurada pelo `thread_id`).

## 3) O agente lembra o nome informado

```bash
python3 -m toolsmith chat --thread kin-nome "Meu nome e Kin"
python3 -m toolsmith chat --thread kin-nome "Qual meu nome mesmo?"
```

**O que esperar**

- A segunda pergunta usa a mesma thread → o agente responde com o nome que você deu (recall entre chamadas no mesmo `thread_id`).

## 4) Inspect — ver o último checkpoint da thread

```bash
python3 -m toolsmith inspect kin-nome
# ou, se o cenario da thread for outro:
python3 -m toolsmith inspect kin-nome --cenario pesquisa
```

**O que esperar**

- `thread: kin-nome (último checkpoint)` seguido de `summary:` (se houver) e as últimas mensagens resumidas (`HumanMessage`/`AIMessage`).

## 5) Listar threads

```bash
python3 -m toolsmith threads
```

**O que esperar**

- Lista os `thread_id` distintos já gravados no sqlite, ex: `default`, `kin-nome`.

---
Ver: `examples/session_b.md` (thread isolada `alice`) · `README.md` (seção Recall/memória).
