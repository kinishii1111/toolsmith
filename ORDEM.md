# ORDEM — tarefa/F2a

## Objetivo

Primeiras **tools do cenário pesquisa** + plugar no grafo from_scratch com loop tool (llm ↔ tools). Sem ouro completo ainda (isso é F2b).

## Copiar de (engenharia reversa)

- ReAct from scratch: ToolNode + `tools_condition` / `should_continue`
  - https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/
  - https://docs.langchain.com/oss/python/langgraph/quickstart
- Busca barata: `duckduckgo-search` **ou** httpx + API simples; se rede falhar no POC, tool pode devolver stub documentado — preferir busca real
- Tools `@tool` com docstring clara (modelo escolhe pela descrição)

## Fazer

1. `src/toolsmith/tools/pesquisa/`: pelo menos **2** tools, ex.:
   - `web_search(query)` → snippets
   - `format_brief(titulo, bullets)` → texto de brief (local, sem LLM obrigatório)
2. `graph_from_scratch.py`: bind tools no LLM **ou**, se sem `GROQ_API_KEY`, modo degradado documentado que ainda chame tools via nó explícito / skip — **preferir** ChatGroq + ToolNode se key existir
3. CLI: `python3 -m toolsmith --cenario pesquisa "o que e LangGraph em 1 frase?"` passa pelo grafo com tools
4. Declarar `duckduckgo-search` (ou escolhido) no `pyproject.toml` se usar
5. README: linha F2a

## Não fazer

- UI, testes, cenário chamado/lead, prebuilt, merge main
- Não exigir query de ouro com fontes perfeitas (F2b)

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F2a && git pull
pip install -e .
# com GROQ_API_KEY no .env (Kin pode ter):
python3 -m toolsmith --cenario pesquisa "capital do Ceara?"
# deve envolver tool (nao so eco F1b). Se sem key: documentar como Kin testa e falhar com mensagem clara.
```

## Tema

Plantão **pesquisa** — busca + brief, 1 motor.
