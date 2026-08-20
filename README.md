# ToolSmith — Plantão de fatos

Agente ReAct (LangGraph): não chuta — despacha **math**, **clima** e **busca**.

> Em construção (micro-tarefas). Ver `ORDEM.md` na branch `tarefa/*`.

## Stack

Python · LangGraph · Groq · Open-Meteo · busca web

## Setup (quando existir deps)

```bash
cp .env.example .env   # GROQ_API_KEY=
pip install -e .
python -m toolsmith "sua pergunta"
```

## Lema

Copiar → preguiça → melhorar → ser esperto.

## Referências (gabarito, não entrega)

- [LangGraph quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [Template `langchain-ai/react-agent`](https://github.com/langchain-ai/react-agent)
