# ToolSmith — Plantão de fatos — 3 plantões, 1 motor

> F0b: pacote roda; agente depois. Zero UI — só CLI.
> F1a: state tipado — `AgentState` com `messages` + `add_messages`.
> F1b: grafo `from_scratch` roda via StateGraph — 1 nó `reply` (echo se sem `GROQ_API_KEY`, senão ChatGroq). `should_continue`/tools ficam pro F2.

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

## Lema

Copiar → preguiça → melhorar → ser esperto. (F0b: engenharia reversa do template → menor diff)

## Referências (gabarito, não entrega)

- [LangGraph quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [Template `langchain-ai/react-agent`](https://github.com/langchain-ai/react-agent)
