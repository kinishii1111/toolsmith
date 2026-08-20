# ORDEM — tarefa/F2b

## Objetivo

**Query de ouro do cenário pesquisa:** pergunta → `web_search` (e se fizer sentido `format_brief`) → resposta final com **fontes/links** visíveis. Loop ReAct de verdade (precisa `GROQ_API_KEY`).

## Copiar de

- Grafo F2a já tem ToolNode + `should_continue`
- Refs ReAct / tool calling LangGraph (mesmas da F2a)
- System prompt curto: “Plantão pesquisa — não invente; cite links das tools”

## Fazer

1. Prompt de sistema / mensagem inicial no `agent` (cenário pesquisa) pedindo citação das URLs retornadas por `web_search`
2. `recursion_limit` razoável no `invoke` (CLI)
3. CLI imprime a resposta final (última AIMessage sem tool_calls)
4. README: como criar `.env` + exemplo de ouro
5. Sem chamado/lead ainda
6. Sem `GROQ_API_KEY`: CLI deve falhar com mensagem clara (exit ≠ 0) — não eco silencioso no modo ouro

## Não fazer

- UI, testes, merge main, outros cenários

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F2b && git pull
# exige .env com GROQ_API_KEY
python3 -m toolsmith --cenario pesquisa "O que e LangGraph? brief curto com fontes"
# resposta cita http/https das tools; NAO so eco
```

## Tema

Plantão pesquisa — ouro com fontes.
