# ORDEM — tarefa/F0b

## Objetivo

Pacote importável + CLI com `--cenario` (pesquisa|chamado|lead) + `python -m toolsmith` → `ToolSmith F0 ok`. Sem agente ainda.

## Copiar de (engenharia reversa)

- Layout pacote: brief `entrada/brief.md` (árvore `src/toolsmith/…`) — adaptar nomes
- Hatch: `pyproject.toml` já tem `packages = ["src/toolsmith"]`
- CLI argparse simples: qualquer `__main__` + `cli.py` mínimo (stdlib)
- Tema travado: 3 cenários, zero UI — job `../TEMA.md`

## Fazer

1. Árvore:
   ```
   src/toolsmith/
     __init__.py
     __main__.py      # chama cli.main
     cli.py           # argparse: --cenario {pesquisa,chamado,lead}; default pesquisa
                      # sem args extras: print "ToolSmith F0 ok [<cenario>]"
     state.py         # stub
     graph_from_scratch.py / graph_prebuilt.py  # stubs
     tools/
       __init__.py
       pesquisa/__init__.py   # stub
       chamado/__init__.py    # stub
       lead/__init__.py       # stub
   diagrams/.gitkeep
   examples/.gitkeep
   ```
2. README: 3 cenários, zero UI, “F0b: pacote roda; agente depois”; lema copiar/reversão
3. Sem LangGraph real, sem HTTP, sem deps novas

## Não fazer

- UI, testes, merge main, utils/, implementar tools de verdade

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F0b && git pull
pip install -e .
python -m toolsmith
python -m toolsmith --cenario chamado
# ambas imprimem ToolSmith F0 ok …
```

## Tema

3 plantões, 1 motor — esqueleto só.
