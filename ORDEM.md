# ORDEM — tarefa/F0a

## Objetivo

Esqueleto de empacotamento + ignore + env de exemplo + README com o tema **Plantão de fatos**. Ainda sem código de agente.

## Copiar de

- Brief do job (estrutura alvo): `../../entrada/brief.md` (relativo ao job; ou peça ao Kin o path absoluto)
- Tema: no job `../TEMA.md` — slogan **Plantão de fatos**, lema copiar/preguiça/melhorar/esperto
- Pyproject mínimo moderno: docs Python packaging / qualquer `pyproject.toml` simples com `[project]` + `[build-system]` hatchling ou setuptools
- Refs LangGraph (só pra citar no README, **não** implementar agora):
  - https://docs.langchain.com/oss/python/langgraph/quickstart
  - https://github.com/langchain-ai/react-agent

## Fazer

1. `pyproject.toml` com nome `toolsmith`, python >=3.11, deps declaradas (ainda podem ser só listadas):
   - `langgraph`, `langchain`, `langchain-groq`, `httpx` (ou `requests`)
   - placeholder busca: comentário Tavily **ou** `duckduckgo-search`
2. `.env.example` com `GROQ_API_KEY=` vazio
3. Garantir `.gitignore` cobre `.env`, venv, `__pycache__`
4. README.md: o que é (Plantão de fatos), o que **não** é (não é Pokédex/chatbot), stack, setup stub, lema em 1 linha
5. Nada em `src/` nesta tarefa (isso é **F0b**)

## Não fazer

- Sem `src/`, sem grafo, sem tools, sem testes, sem UI
- Sem chave real no repo
- Sem inventar pasta `utils/` / `services/`

## Pronto quando

Kin vê no repo:

- `pyproject.toml`, `.env.example`, `.gitignore`, `README.md`
- README menciona **Plantão de fatos** e o lema

```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith
git status
ls pyproject.toml .env.example README.md
```

## Tema

Plantão de fatos — despachante que não chuta.
