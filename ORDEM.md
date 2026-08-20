# ORDEM — tarefa/F1a

## Objetivo

`state.py` tipado com `messages` + reducer (LangGraph/AddableValues). Só estado — sem grafo rodando ainda.

## Copiar de (engenharia reversa)

- Quickstart / ReAct from scratch: TypedDict state com `Annotated[list, add_messages]`
  - https://docs.langchain.com/oss/python/langgraph/quickstart
  - https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch-functional/
- Template: https://github.com/langchain-ai/react-agent (arquivo de state/graph)
- Pacote já existe em `src/toolsmith/`; `pyproject` já declara langgraph

## Fazer

1. Implementar `src/toolsmith/state.py`:
   - `AgentState` (ou nome curto) com `messages` usando `add_messages`
   - Docstring 2 linhas: estado compartilhado dos 3 cenários
2. Garantir imports resolvem: `from toolsmith.state import …`
3. Não ligar LLM/tools/grafo nesta tarefa
4. README: 1 linha “F1a: state tipado”

## Não fazer

- UI, testes, CLI nova, implementar tools, merge main

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F1a && git pull
python -c "from toolsmith.state import AgentState; print('F1a ok', AgentState)"
```

(Ajuste o nome da classe se copiar outro das refs — documente no Resultado do commit.)

## Tema

3 plantões, 1 motor — estado único.
