# ORDEM — tarefa/F5b

## Objetivo

Fechar Nível 1 pro currículo: **diagrama Mermaid** do grafo, `examples/demo.md` com **1 ouro por cenário** (traces curtos), README de portfólio (PT + EN curto).

## Copiar de

- Brief do job (bullets currículo)
- TEMA: 3 plantões, 1 motor
- Pastas `diagrams/`, `examples/`

## Fazer

1. `diagrams/graph.mmd` — loop agent ↔ tools → end (Mermaid)
2. `examples/demo.md` — 3 seções (pesquisa / chamado / lead) pergunta → tools → trecho resposta
3. README: arquitetura, `.env`, `--cenario`, `--motor`, scratch vs prebuilt, fora de escopo Nível 2+, 1 linha LinkedIn (PT + EN curto)
4. Sem UI/testes

## Não fazer

- UI, testes, merge main, Nível 2+

## Pronto quando

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git checkout tarefa/F5b && git pull
test -f diagrams/graph.mmd && test -f examples/demo.md
rg -n "Plantão|--cenario|from_scratch" README.md
```

## Tema

Plantão de fatos — entrega de currículo.
