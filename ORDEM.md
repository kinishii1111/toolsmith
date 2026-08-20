# ORDEM — tarefa/F5a

## Objetivo

Versão **prebuilt** (`create_react_agent` ou equivalente atual LangGraph) para **comparar** com `from_scratch`. Mesmos tools do cenário. CLI flag `--motor scratch|prebuilt` (default scratch).

## Copiar de

- https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/
- Docs atuais `langgraph.prebuilt` (nome pode ser `create_react_agent`)
- Tools já em pesquisa/chamado/lead

## Fazer

1. `graph_prebuilt.py`: `build_graph(cenario)` usando prebuilt + mesmos TOOLS/prompt do scratch
2. CLI: `--motor {scratch,prebuilt}`; scratch = `graph_from_scratch`
3. README: por que StateGraph from scratch vs prebuilt (2–4 linhas currículo)
4. Sem UI/testes

## Não fazer

- UI, testes, merge main, Mermaid/demos (F5b)

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F5a && git pull
python3 -m toolsmith --motor prebuilt --cenario pesquisa "capital do Ceara em 1 frase"
python3 -m toolsmith --motor scratch --cenario pesquisa "capital do Ceara em 1 frase"
# ambos respondem sem traceback
```

## Tema

1 motor ensinado de 2 jeitos — comparar.
