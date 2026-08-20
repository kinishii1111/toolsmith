# ORDEM — tarefa/F4a

## Objetivo

Cenário **lead**: tools score + tag + draft reply; plugar no grafo; **ouro** numa tacada (msg crua → qualificado + resposta + tag).

## Copiar de

- Padrão `@tool` de `chamado/` / `pesquisa/`
- `build_graph(cenario=...)` já troca TOOLS + system prompt
- Regras ICP locais em dict/arquivo `tools/lead/regras.md` (orçamento, urgência, segmento)

## Fazer

1. Tools `tools/lead/`:
   - `score_lead(texto)` → 0–100 + motivos (heurística)
   - `tag_lead(texto)` → tags tipo `quente|morno|frio`, `b2b|b2c`
   - `draft_lead_reply(texto, score, tags)` → rascunho WhatsApp/e-mail curto
2. System prompt lead: use as 3 tools; termine com `SCORE:` e `TAGS:`
3. README: exemplo ouro lead
4. Pesquisa + chamado intactos

## Não fazer

- UI, CRM real, testes, merge main, prebuilt (F5)

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F4a && git pull
python3 -m toolsmith --cenario lead "Oi, tenho empresa de 50 funcionarios, preciso de proposta essa semana, orcamento ate 20k"
# SCORE: … TAGS: … e rascunho util
```

## Tema

Plantão lead — qualificar + responder.
