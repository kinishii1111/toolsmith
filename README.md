# ToolSmith — Plantão de fatos — 3 plantões, 1 motor

> F0b: pacote roda; agente depois. Zero UI — só CLI.
> F1a: state tipado — `AgentState` com `messages` + `add_messages`.
> F1b: grafo `from_scratch` roda via StateGraph — 1 nó `reply` (echo se sem `GROQ_API_KEY`, senão ChatGroq). `should_continue`/tools ficam pro F2.
> F2a: tools do cenário **pesquisa** — `web_search` (ddgs/DuckDuckGo) + `format_brief`; grafo from_scratch com loop tool (llm ↔ ToolNode). Sem `GROQ_API_KEY` o nó `agent` ecoa e não chama tools (modo degradado documentado).
> F2b: ouro do cenário **pesquisa** — `agent` pede que a resposta final cite as URLs retornadas por `web_search`; CLI imprime só a resposta final e exige `GROQ_API_KEY` (sem key sai com erro, exit ≠ 0).
> F3a: kit **chamado** — tools locais `classify_ticket`/`search_kb`/`draft_reply` + KB `kb/*.md` + `build_graph(cenario)` seleciona kit (pesquisa continua funcionando).
> F3b: ouro **chamado** — system prompt exige severidade + trecho KB + rascunho + `ESCALAR: sim|nao — motivo`; `recursion_limit` no invoke; pesquisa continua ok.
> F4a: kit **lead** — tools locais `score_lead`/`tag_lead`/`draft_lead_reply` + regras ICP `tools/lead/regras.md` + ouro 1 tacada (qualificar+responder+tag) com `SCORE:` e `TAGS:`.
> F5a: **scratch vs prebuilt** — `StateGraph` from scratch expõe nós/arestas e `should_continue` (didático, controle total); `create_react_agent` (prebuilt) entrega o mesmo loop ReAct pronto; mesmos TOOLS/prompt, flag `--motor scratch|prebuilt`.

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

Ouro lead (qualificar + responder + tag — 1 tacada):

```bash
python3 -m toolsmith --cenario lead "Oi, tenho empresa de 50 funcionarios, preciso de proposta essa semana, orcamento ate 20k"
# rascunho WhatsApp/e-mail curto + SCORE: … e TAGS: quente, b2b (heurística via tools/lead/regras.md)
```

Sem `GROQ_API_KEY` o CLI sai com erro claro (exit ≠ 0) — não ecoa silenciosamente.

## Arquitetura — loop agent ↔ tools → end

```
START → agent (ChatGroq bind_tools + SystemPrompt por cenário)
       → should_continue { tool_calls? } → tools (ToolNode) → agent → ... → END
       invoke {messages:[HumanMessage]} recursion_limit 20 → última AIMessage sem tool_calls
```

State: `AgentState` (`messages: Annotated[list, add_messages]`) — um state para 3 Plantões.
Diagrama Mermaid: `diagrams/graph.mmd` (renderize no GitHub/Mermaid Live).
Demos ouro por cenário: `examples/demo.md` (pesquisa/chamado/lead — pergunta → tools → trecho resposta).

## Setup — .env e --cenario / --motor

```bash
cp .env.example .env   # GROQ_API_KEY=gsk_...
# CLI lê GROQ_API_KEY do ambiente; .env carregado via python-dotenv ou: set -a; source .env; set +a
pip install -e .
python -m toolsmith --cenario pesquisa "O que e LangGraph? brief curto com fontes"
python -m toolsmith --cenario chamado  "Desde ontem nao consigo logar, preciso urgente"
python -m toolsmith --cenario lead     "empresa 50 funcionarios, proposta essa semana, orcamento 20k"
# motores: --motor scratch (default, StateGraph from_scratch, nós/arestas + should_continue expostos)
#        | --motor prebuilt (create_react_agent, mesmo loop ReAct pronto; mesmos TOOLS/prompt)
python -m toolsmith --motor prebuilt --cenario pesquisa "ping"
```

Sem `GROQ_API_KEY` o CLI sai com erro claro (`exit != 0`) — não ecoa silenciosamente.

## Scratch vs prebuilt — 1 motor, 2 jeitos

| Motor | Arquivo | O que expõe | Quando usar |
|-------|---------|-------------|-------------|
| `scratch` (`from_scratch`) | `src/toolsmith/graph_from_scratch.py` | `StateGraph(AgentState)`, `add_node("agent"/"tools")`, `add_conditional_edges(should_continue)`, `ToolNode(TOOLS)` — controle total/didático | portfólio currículo Nível 1, explicar loop |
| `prebuilt` | `src/toolsmith/graph_prebuilt.py` | `create_react_agent(model, TOOLS, prompt)` — mesmo loop pronto | prod / menos boilerplate |

Mesmos `TOOLS` e `SYSTEM_PROMPT` por `--cenario` (`_get_tools_and_prompt`): pesquisa (`web_search`/`format_brief`), chamado (`classify_ticket`/`search_kb`/`draft_reply` + `kb/*.md`), lead (`score_lead`/`tag_lead`/`draft_lead_reply` + `tools/lead/regras.md`). Flag `--motor scratch|prebuilt` troca só o builder.

## Fora de escopo — Nível 2+

Nível 1 (currículo) fecha aqui: diagrama + `examples/demo.md` + README PT+EN. Fica fora:

- UI (Streamlit/Gradio), testes automatizados, `merge main`, deploy, auth, persistência, memória longa, multi-agente, HITL, avaliação/RAG avançado, guardrails.

## Currículo — 1 linha

PT: Agente ReAct LangGraph (Groq) — 3 Plantões (pesquisa/chamado/lead), 1 motor em 2 jeitos (`scratch`/`prebuilt`), loop `agent ↔ tools → end` com `--cenario`/`--motor` e ouro por cenário. · EN: ReAct agent on LangGraph (Groq) — 3 shifts, 1 engine (scratch vs prebuilt), `agent ↔ tools → end` loop with `--cenario`/`--motor` and golden traces per scenario.

## Lema

Copiar → preguiça → melhorar → ser esperto. (F0b: engenharia reversa do template → menor diff)

## Referências (gabarito, não entrega)

- [LangGraph quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [Template `langchain-ai/react-agent`](https://github.com/langchain-ai/react-agent)
