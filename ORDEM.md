# ORDEM — tarefa/r2-wire-graph-fix

## Agente
opencode

## Objetivo
Corrigir review: o nó summarize está errado — entry sempre chama summarize_node e ele corta pra KEEP_LAST mesmo com poucas msgs.

## Copiar de
- Diff/erro: em graph_from_scratch, entry=`summarize` + summarize_node sempre trunca se len>4. Correto: só compactar quando should_summarize.

## Fazer
1. Em `src/toolsmith/graph_from_scratch.py` apenas:
   - Entry = **agent** OU entry condicional: se `should_summarize` → nó que chama `summarize_node` **uma vez** → agent; senão → agent.
   - Proibido: entry sempre em summarize_node; proibido edge `summarize`→`summarize` (loop).
   - Padrão preferido:
     ```
     START → route_summarize
       True  → summarize (summarize_node) → agent
       False → agent
     agent → tools|end …
     ```
     Use `graph.add_conditional_edges` a partir de um nó passthrough mínimo OU `graph.set_conditional_entry_point` se existir na API.
   - `summarize_node` só deve rodar quando `should_summarize` for True.
2. Não mexer em graph_prebuilt além do que já está (checkpointer ok).
3. Commit + push na mesma branch `tarefa/r2-wire-graph`.

## Arquivos permitidos
- src/toolsmith/graph_from_scratch.py
- ORDEM.md
- NÃO abrir mais nada

## Não fazer
- Sem CLI / merge main / explorar repo
- Sem mudar summarize.py (o bug é o wire)

## Ownership
- src/toolsmith/graph_from_scratch.py

## Pronto quando
```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith-wt-tarefa-r2-wire-graph
PYTHONPATH=src python3 -c "
from langchain_core.messages import HumanMessage
from toolsmith.graph_from_scratch import build_graph
from toolsmith.memory import get_checkpointer
import tempfile
p=tempfile.mktemp(suffix='.sqlite')
g=build_graph('pesquisa', checkpointer=get_checkpointer(p))
# 5 msgs: NÃO deve truncar pra 4 só por passar no grafo sem tool — invoke ping curto
r=g.invoke({'messages':[HumanMessage(content='oi')],'summary':''}, config={'configurable':{'thread_id':'t1'},'recursion_limit':8})
assert len(r['messages']) >= 1
print('ok', type(g).__name__, 'msgs', len(r['messages']))
"
```

## Tema
Bounce: summarize só quando should_summarize
