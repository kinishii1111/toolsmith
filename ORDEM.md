# ORDEM — tarefa/F1b

## Objetivo

Grafo **from_scratch** mínimo + CLI aceitando uma pergunta (cenário `pesquisa` default). Ainda sem tools reais — 1 nó LLM **ou** echo controlado que prove o StateGraph rodando.

Preferência Nível 1 / preguiça: se Groq/key complicar agora, um nó `reply` que devolve mensagem fixa/eco da pergunta **via StateGraph** (não print solto) já serve — documente no README. Ideal: ChatGroq se `.env` tiver chave.

## Copiar de

- https://docs.langchain.com/oss/python/langgraph/quickstart (StateGraph + compile + invoke)
- State já em `toolsmith.state.AgentState`
- CLI atual: estender para positional `pergunta` opcional

## Fazer

1. `graph_from_scratch.py`: `build_graph()` → `StateGraph(AgentState)` com ≥1 nó que lê/escreve `messages`, `compile()`
2. `cli.py`: `python -m toolsmith "ola"` (e `--cenario`) chama o grafo e imprime a última mensagem
3. Sem tools ainda; `should_continue` pode ficar pro F2
4. README: linha F1b

## Não fazer

- UI, testes, tools pesquisa/chamado/lead, prebuilt completo, merge main

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F1b && git pull
python3 -m toolsmith "ping"
# imprime resposta vinda do grafo (não só F0 ok)
```

## Tema

1 motor, cenário pesquisa default — loop ainda sem tools.
