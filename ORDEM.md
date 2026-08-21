# ORDEM — tarefa/r3-docs

## Agente
opencode

## Objetivo
README + examples das 2 sessões Recall (Plantão) + atualizar diagrama se fácil.

## Copiar de
- README atual (N1)
- Ouro: thread kin nome+SP → restart → pergunta nome; thread alice isolada
- CLI: `toolsmith chat --thread`, `threads`, `inspect`

## Fazer
1. Atualizar `README.md`: seção Recall/memória (SqliteSaver, thread_id, summarize, stream); como testar 2 sessões; link plantões; fora Postgres/HITL/UI
2. `examples/session_a.md` e `examples/session_b.md` (comandos + o que esperar)
3. Se `diagrams/graph.mmd` existir: acrescentar nó summarize opcional (1–3 linhas)
4. NÃO mudar código src/

## Arquivos permitidos
- README.md
- examples/session_a.md
- examples/session_b.md
- diagrams/graph.mmd
- ORDEM.md

## Não fazer
- Sem UI / testes / merge main / explorar além do permitido

## Ownership
- README.md
- examples/
- diagrams/graph.mmd

## Pronto quando
```bash
test -f examples/session_a.md && test -f examples/session_b.md && grep -qi thread README.md && echo docs_ok
```

## Tema
Recall N2 — docs currículo
