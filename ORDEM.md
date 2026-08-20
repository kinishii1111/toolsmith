# ORDEM — tarefa/r1-memory

## Agente
opencode

## Objetivo
Criar fábrica SqliteSaver + pasta data/ ignorando .sqlite. Base do Recall (N2) sem tocar no grafo/CLI.

## Copiar de
- Docs: https://docs.langchain.com/oss/python/langgraph/persistence (SqliteSaver + thread_id)
- Pacote: `langgraph-checkpoint-sqlite` (import típico: `from langgraph.checkpoint.sqlite import SqliteSaver`)
- NÃO copiar math/clima do brief antigo — só memória

## Fazer
1. Em `pyproject.toml`: adicionar dependência `langgraph-checkpoint-sqlite` (não mudar o resto sem necessidade).
2. Criar `src/toolsmith/memory.py` com:
   - `DEFAULT_DB` = path absoluto ou relativo à raiz do repo: `data/checkpoints.sqlite`
   - `get_checkpointer(db_path=None)` → retorna `SqliteSaver` (usar context manager / `from_conn_string` conforme a API do pacote instalado — se a API exigir `with`, expor helper que abre conexão e devolve saver usável em `compile(checkpointer=…)`)
   - Docstring curta: memória por `thread_id`, não Store longo prazo
3. Criar `data/.gitkeep` e em `.gitignore` adicionar: `data/*.sqlite` e `data/*.sqlite-*` (wal/shm)
4. NÃO alterar graph_*.py, cli.py, state.py, tools/, README

## Arquivos permitidos
- pyproject.toml
- src/toolsmith/memory.py
- data/.gitkeep
- .gitignore
- ORDEM.md
- NÃO abrir mais nada

## Não fazer
- Sem testes / UI / merge main / explorar repo / ler README inteiro
- Sem alterar grafo ou CLI (onda seguinte)
- Sem hardcodar modelo LLM
- Sem commitar .env ou .sqlite

## Ownership
- pyproject.toml
- src/toolsmith/memory.py
- data/
- .gitignore

## Pronto quando
```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
pip install -e . -q
python3 -c "from toolsmith.memory import get_checkpointer; c=get_checkpointer(); print(type(c).__name__)"
```
(deve imprimir algo com Sqlite / Saver; se API for context manager, o helper deve retornar objeto já pronto ou documentar uso no docstring e o comando acima ainda deve funcionar)

## Tema
Recall N2 — checkpoint SQLite no Plantão
