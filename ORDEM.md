# ORDEM — tarefa/F3a

## Objetivo

Kit **chamado**: tools locais (classificar + buscar KB + rascunhar) plugadas no mesmo grafo, selecionáveis via `--cenario chamado`. Ainda sem ouro completo (F3b).

## Copiar de

- Padrão `@tool` + ToolNode de `tools/pesquisa/`
- Grafo: trocar TOOLS conforme `cenario` (CLI passa cenario → `build_graph(cenario=...)`)
- KB: arquivos markdown em `src/toolsmith/tools/chamado/kb/*.md` (2–3 FAQs inventadas, curtas)

## Fazer

1. Tools em `tools/chamado/`:
   - `classify_ticket(texto)` → severidade/categoria (heurística local ok)
   - `search_kb(query)` → trechos dos md em `kb/`
   - `draft_reply(contexto, tom="objetivo")` → rascunho local (template string ok; sem exigir LLM na tool)
2. `build_graph(cenario: str)` escolhe TOOLS + system prompt do cenário
3. CLI passa `args.cenario` pro grafo
4. README: linha F3a + exemplo ticket
5. Manter pesquisa funcionando

## Não fazer

- UI, testes, lead, merge main, RAG vetorial

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F3a && git pull
# com .env
python3 -m toolsmith --cenario chamado "Cliente diz que o login nao funciona desde ontem e esta com pressa"
# deve usar tools de chamado (nao so eco); idealmente menciona classify/kb no rastro ou na resposta
```

## Tema

Plantão chamado — triage + KB local.
