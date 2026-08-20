# Demo — Plantão de fatos — 1 ouro por cenário (traces curtos)

> Requisitos: `GROQ_API_KEY` no `.env` (ver README). Sem key o CLI sai com erro (`exit != 0`). Grafo usa `recursion_limit: 20` e loop `agent ↔ tools → end` (ver `diagrams/graph.mmd`).

---

## 1) Plantão pesquisa — pergunta → tools → resposta com fontes

**Pergunta**

```bash
python3 -m toolsmith --cenario pesquisa "O que e LangGraph? brief curto com fontes"
# --motor scratch|prebuilt (mesmos TOOLS/prompt)
```

**Tools despachadas (kit `pesquisa`)**

- `web_search("O que e LangGraph")` → snippets com `title + href + body` (ddgs/DuckDuckGo; stub documentado se rede falhar)
- `format_brief(resultados)` → brief citável

**Trecho resposta (ouro — cita URLs)**

```
LangGraph é framework de grafos para agentes ReAct (LangChain) — state `AgentState` + nós `agent/tools` + `should_continue`.

Fontes:
- https://docs.langchain.com/oss/python/langgraph/quickstart
- https://github.com/langchain-ai/react-agent
- [URL retornada por web_search]

> Ouro F2b: `agent` só responde citando as URLs que `web_search` retornou.
```

---

## 2) Plantão chamado — pergunta → tools → severidade + KB + ESCALAR

**Pergunta**

```bash
python3 -m toolsmith --cenario chamado "Desde ontem nao consigo logar, preciso urgente, ja tentei reset e nada"
```

**Tools despachadas (kit `chamado`)**

- `classify_ticket(texto)` → `Severidade: alta | Categoria: login`
- `search_kb("login")` → trecho `kb/login.md` (ex: reset/limpar cache/contatar N2)
- `draft_reply(classificação + trecho KB)` → rascunho

**Trecho resposta (ouro — linha final obrigatória)**

```
Severidade: alta | Categoria: login
Trecho KB (kb/login.md): "Se login falha há >24h mesmo após reset, orientar limpar cache e, se persistir, escalar para N2..."

Olá! Entendi a urgência — vamos resolver seu acesso. Tente ... [rascunho de draft_reply] ...
ESCALAR: sim — alta+sem reset ha >24h, exige N2
```

---

## 3) Plantão lead — pergunta → tools → rascunho + SCORE + TAGS (1 tacada)

**Pergunta**

```bash
python3 -m toolsmith --cenario lead "Oi, tenho empresa de 50 funcionarios, preciso de proposta essa semana, orcamento ate 20k"
```

**Tools despachadas (kit `lead` — regras em `tools/lead/regras.md`)**

- `score_lead(texto)` → `SCORE: 100 | Motivos: base 20; orçamento até 20k explícito +30; urgência/proposta essa semana +25; segmento B2B/empresa +25; porte >=20 funcionários +5`
- `tag_lead(texto)` → `quente, b2b` (quente ≥70)
- `draft_lead_reply(texto)` → rascunho WhatsApp/e-mail curto

**Trecho resposta (ouro — 2 linhas finais obrigatórias)**

```
Oi! Obrigado pelo contato — com 50 funcionários e orçamento até 20k conseguimos montar proposta ainda essa semana. Que tal uma call de 20min amanhã para alinhar escopo e prazos? ...

SCORE: 85
TAGS: quente, b2b
```

---
Diagrama: `diagrams/graph.mmd` — `START → agent → should_continue → tools → agent → ... → END`
Motores: `--motor scratch` (StateGraph `from_scratch`, `should_continue` exposto) vs `--motor prebuilt` (`create_react_agent`, mesmo loop pronto).
