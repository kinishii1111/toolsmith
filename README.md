# ToolSmith — Plantão de fatos — 3 plantões, 1 motor

> F0b: pacote roda; agente depois. Zero UI — só CLI.
> F1a: state tipado — `AgentState` com `messages` + `add_messages`.
> F1b: grafo `from_scratch` roda via StateGraph — 1 nó `reply` (echo se sem `GROQ_API_KEY`, senão ChatGroq). `should_continue`/tools ficam pro F2.
> F2a: tools do cenário **pesquisa** — `web_search` (ddgs/DuckDuckGo) + `format_brief`; grafo from_scratch com loop tool (llm ↔ ToolNode). Sem `GROQ_API_KEY` o nó `agent` ecoa e não chama tools (modo degradado documentado).
> F2b: ouro do cenário **pesquisa** — `agent` pede que a resposta final cite as URLs retornadas por `web_search`; CLI imprime só a resposta final e exige `GROQ_API_KEY` (sem key sai com erro, exit ≠ 0).
> F3a: kit **chamado** — tools locais `classify_ticket`/`search_kb`/`draft_reply` + KB `kb/*.md` + `build_graph(cenario)` seleciona kit (pesquisa continua funcionando).
> F3b: ouro **chamado** — system prompt exige severidade + trecho KB + rascunho + `ESCALAR: sim|nao — motivo`; `recursion_limit` no invoke; pesquisa continua ok.

Agente ReAct (LangGraph): não chuta — despacha por cenário.

| Cenário | Kit (F1) |
|---------|----------|
| `pesquisa` | busca · extrair · brief |
| `chamado` | classificar · base local · rascunho |
| `lead` | score · tag · reply |

> Em construção (micro-tarefas). Ver `ORDEM.md` na branch `tarefa/*`.

## Stack

Python · LangGraph · Groq · Open-Meteo · busca web

## Setup

```bash
cp .env.example .env   # GROQ_API_KEY=
pip install -e .
python -m toolsmith
python -m toolsmith --cenario chamado
python -m toolsmith --cenario lead
```

Criar `.env` (o CLI lê de `GROQ_API_KEY` no ambiente; o `.env` é carregado pela shell ou `set -a; source .env; set +a`):

```bash
cp .env.example .env
# edite .env e cole sua chave: GROQ_API_KEY=gsk_...
```

Exemplo de ouro (pesquisa com fontes):

```bash
python3 -m toolsmith --cenario pesquisa "O que e LangGraph? brief curto com fontes"
```

Exemplo ticket (chamado):

```bash
python3 -m toolsmith --cenario chamado "Cliente diz que o login nao funciona desde ontem e esta com pressa"
```

Ouro chamado (triage + escalação):

```bash
python3 -m toolsmith --cenario chamado "Desde ontem nao consigo logar, preciso urgente, ja tentei reset e nada"
# saída com severidade, trecho KB/login e linha final ESCALAR: sim|nao — motivo
```

Sem `GROQ_API_KEY` o CLI sai com erro claro (exit ≠ 0) — não ecoa silenciosamente.

## Lema

Copiar → preguiça → melhorar → ser esperto. (F0b: engenharia reversa do template → menor diff)

## Referências (gabarito, não entrega)

- [LangGraph quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [Template `langchain-ai/react-agent`](https://github.com/langchain-ai/react-agent)
