# ORDEM — tarefa/F0b

## Objetivo

Pacote Python importável + `python -m toolsmith` imprimindo `ToolSmith F0 ok` (Plantão de fatos). Ainda sem agente/tools.

## Copiar de

- Layout do brief: `src/toolsmith/` com stubs (`__init__`, `__main__`, `cli`, `state`, graphs, `tools/*`)
- Hatch já aponta `packages = ["src/toolsmith"]` no `pyproject.toml` (F0a)
- Padrão `__main__.py` chama `cli.main`

## Fazer

1. Criar árvore:
   ```
   src/toolsmith/
     __init__.py
     __main__.py
     cli.py          # main() printa ToolSmith F0 ok
     state.py        # stub (pass ou docstring)
     graph_from_scratch.py  # stub
     graph_prebuilt.py      # stub
     tools/
       __init__.py
       math.py / weather.py / search.py  # stubs
   ```
2. `diagrams/.gitkeep` e `examples/.gitkeep`
3. README: uma linha “F0b: pacote roda; agente ainda não”
4. Não implementar LangGraph/tools de verdade

## Não fazer

- Sem LLM, sem HTTP, sem deps novas no pyproject
- Sem testes, UI, merge main
- Sem pasta utils/services

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
pip install -e .     # se ainda não
python -m toolsmith  # → ToolSmith F0 ok
```

## Tema

Plantão de fatos — esqueleto só; despacho vem depois.
