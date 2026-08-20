# ORDEM — tarefa/F3b

## Objetivo

**Ouro chamado:** ticket ambíguo/urgente → classify + search_kb → draft com indicação clara de **escalar ou não** (e por quê).

## Copiar de

- Kit F3a já no grafo via `--cenario chamado`
- System prompt pesquisa: espelhar tom “não invente; use tools; diga se escala”

## Fazer

1. System prompt `chamado` pedindo: severidade, trecho KB, rascunho, linha final `ESCALAR: sim|nao — motivo`
2. Garantir `recursion_limit` no invoke (já existe)
3. README: exemplo ouro chamado
4. Pesquisa continua ok

## Não fazer

- UI, lead, testes, merge main

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F3b && git pull
python3 -m toolsmith --cenario chamado "Desde ontem nao consigo logar, preciso urgente, ja tentei reset e nada"
# saida com ESCALAR: … e rastro util (KB/login)
```

## Tema

Plantão chamado — ouro triage + escalação.
