# ORDEM — tarefa/r1-summarize

## Agente
claude

## Objetivo
Nó/função de resumo de histórico + campo `summary` no state. Sem ligar no grafo ainda.

## Copiar de
- Padrão LangGraph: se len(messages) > N, compactar antigas; manter as K últimas intactas
- Brief: summarize não apaga a última pergunta
- State atual: `src/toolsmith/state.py` (só messages hoje)

## Fazer
1. Em `src/toolsmith/state.py`: adicionar `summary: str` (default conceitual vazio; TypedDict pode usar `NotRequired` ou `total=False` só se necessário — manter `messages` com `add_messages`)
2. Criar `src/toolsmith/summarize.py` com:
   - Constantes `SUMMARIZE_AFTER = 12` e `KEEP_LAST = 4` (ajustáveis no topo)
   - `should_summarize(state) -> bool`
   - `summarize_node(state) -> dict` atualizando `summary` e **encurtando** `messages` (antigas viram texto no summary; últimas K ficam). Sem LLM se não houver GROQ_API_KEY: summary = junção truncada dos contents antigos. Com key: 1 call ChatGroq modelo `openai/gpt-oss-20b` (ou listar models se esse id falhar — não inventar id morto tipo llama-3.3-70b-versatile).
   - Função pura / nó: **não** importar graph_*.py
3. NÃO alterar memory.py, cli, graph, tools, pyproject, README

## Arquivos permitidos
- src/toolsmith/state.py
- src/toolsmith/summarize.py
- ORDEM.md
- NÃO abrir mais nada

## Não fazer
- Sem testes / UI / merge main / explorar repo / ler README
- Sem wire no grafo (onda 2)
- Sem tocar pyproject / memory.py

## Ownership
- src/toolsmith/state.py
- src/toolsmith/summarize.py

## Pronto quando
```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
PYTHONPATH=src python3 -c "
from toolsmith.summarize import should_summarize, summarize_node, SUMMARIZE_AFTER
from langchain_core.messages import HumanMessage
st={'messages':[HumanMessage(content=f'msg{i}') for i in range(SUMMARIZE_AFTER+1)], 'summary':''}
assert should_summarize(st)
out=summarize_node(st)
assert 'summary' in out and out['summary']
assert len(out['messages']) <= 4+1
print('ok', len(out['messages']), out['summary'][:60])
"
```

## Tema
Recall N2 — compactar histórico Plantão
