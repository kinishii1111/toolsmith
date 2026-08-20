# ORDEM — tarefa/r2-wire-graph

## Agente
opencode

## Objetivo
Ligar SqliteSaver + nó summarize no grafo scratch (e prebuilt se a API permitir). Sem CLI ainda.

## Copiar de
- `src/toolsmith/memory.py` → `get_checkpointer()`
- `src/toolsmith/summarize.py` → `should_summarize` / `summarize_node`
- Docs Persistence: `compile(checkpointer=...)` + `config={"configurable":{"thread_id":"..."}}`
- Grafo atual: `src/toolsmith/graph_from_scratch.py` (entry = agent)

## Fazer
1. Em `graph_from_scratch.py`:
   - `build_graph(cenario=..., checkpointer=None)` — se `checkpointer` None, chamar `get_checkpointer()`
   - Antes do `agent`: nó `summarize` (condicional: se `should_summarize` → `summarize_node`, senão passa adiante). Entry point = summarize (ou edge START→summarize→agent).
   - `return graph.compile(checkpointer=checkpointer)`
2. Em `graph_prebuilt.py`: passar `checkpointer` em `create_react_agent` / `compile` conforme API atual do pacote (se prebuilt não aceitar nó summarize fácil, só checkpointer + docstring “summarize só no scratch”).
3. NÃO alterar cli.py, tools/, README, pyproject (já tem dep).

## Arquivos permitidos
- src/toolsmith/graph_from_scratch.py
- src/toolsmith/graph_prebuilt.py
- ORDEM.md
- NÃO abrir mais nada (pode ler memory.py/summarize.py/state.py só se import precisar — não editar)

## Não fazer
- Sem CLI / stream / threads command (onda 2b)
- Sem testes / UI / merge main / explorar repo
- Sem mudar prompts dos plantões

## Ownership
- src/toolsmith/graph_from_scratch.py
- src/toolsmith/graph_prebuilt.py

## Pronto quando
```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
PYTHONPATH=src python3 -c "
from toolsmith.graph_from_scratch import build_graph
from toolsmith.memory import get_checkpointer
g=build_graph('pesquisa', checkpointer=get_checkpointer(':memory:'))
print('ok', type(g).__name__)
"
```
(Se `:memory:` não rolar no helper, use path temp em /tmp/t.sqlite)

## Tema
Recall N2 — wire memória no Plantão
