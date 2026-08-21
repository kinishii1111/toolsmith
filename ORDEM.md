# ORDEM — tarefa/r2-cli

## Agente
opencode

## Objetivo
CLI Recall: `--thread`, stream, `threads` e `inspect`. Grafo já tem checkpointer.

## Copiar de
- `src/toolsmith/cli.py` atual
- `src/toolsmith/memory.py` DEFAULT_DB
- Brief: `python -m toolsmith --thread kin "..."` + subcomandos threads/inspect

## Fazer
1. Em `cli.py`:
   - Flag `--thread ID` (default `default`) → `config={"configurable":{"thread_id": ID}, "recursion_limit": 20}`
   - Em invoke/stream: passar config; carregar histórico via checkpointer (invoke com messages novas só — LangGraph mergeia)
   - Streaming: se stdout TTY ou flag `--stream`, usar `graph.stream(..., stream_mode="messages")` e printar tokens/chunks; senão `invoke`
   - Subcomando ou modo: `threads` lista thread_ids do sqlite (consultar API SqliteSaver / sql na DEFAULT_DB)
   - `inspect THREAD` imprime último checkpoint (summary + últimas msgs resumidas)
   - Manter `--cenario` e `--motor`
2. `.gitignore` já ignora sqlite — ok
3. NÃO reescrever graphs (só importar build_*)

## Arquivos permitidos
- src/toolsmith/cli.py
- ORDEM.md
- NÃO abrir mais nada (ler memory.py ok sem editar)

## Não fazer
- Sem UI / testes / merge main / README grande
- Sem Postgres

## Ownership
- src/toolsmith/cli.py

## Pronto quando
```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
rm -f /tmp/recall-test.sqlite
PYTHONPATH=src TOOLSMITH_CHECKPOINT=/tmp/recall-test.sqlite python3 -c "
# se cli não ler env, use default data/ — ok testar --help
import toolsmith.cli as c
print('cli_ok', hasattr(c,'main'))
"
PYTHONPATH=src python3 -m toolsmith --help
```
(Deve mostrar --thread e/ou threads/inspect sem crash)

## Tema
Recall N2 — CLI thread + stream
