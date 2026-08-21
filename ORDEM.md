# ORDEM — tarefa/r2-cli-fix

## Agente
opencode

## Objetivo
Corrigir review: `python -m toolsmith "ping"` quebrou (argparse trata "ping" como subcomando). Manter `threads`/`inspect`/`chat` e restaurar legado.

## Copiar de
- Erro: `invalid choice: 'ping' (choose from 'threads', 'inspect', 'chat')`
- Queremos: `toolsmith "pergunta" --thread kin` E `toolsmith chat "pergunta" --thread kin` E `toolsmith threads` / `inspect`

## Fazer
1. Só `src/toolsmith/cli.py`:
   - Se argv[1] ∈ {threads, inspect, chat} → subparsers (como agora)
   - Senão → modo legado/chat: flags `--thread`, `--stream`, `--cenario`, `--motor` + pergunta posicional (default ping)
   - Uma forma simples: pré-parse / se primeiro arg não é comando conhecido, inserir `chat` no argv antes do parse
2. Garantir: sem GROQ_API_KEY no chat → exit 1 mensagem clara; `threads`/`inspect` sem key ok
3. Commit + push mesma branch

## Arquivos permitidos
- src/toolsmith/cli.py
- ORDEM.md

## Não fazer
- Sem merge main / README / graphs

## Ownership
- src/toolsmith/cli.py

## Pronto quando
```bash
cd /home/kin/Documents/estudo/langgraph-portfolio/trabalho/toolsmith-wt-tarefa-r2-cli
PYTHONPATH=src python3 -m toolsmith --help
PYTHONPATH=src python3 -m toolsmith chat --help | grep -q thread
# legado não pode crashar no parse:
PYTHONPATH=src python3 -c "import sys; sys.argv=['toolsmith','ping','--thread','t']; from toolsmith.cli import main" 2>&1 | head -3
# (pode pedir GROQ_API_KEY — OK; NÃO pode 'invalid choice: ping')
GROQ_API_KEY= PYTHONPATH=src python3 -m toolsmith ping 2>&1 | grep -v 'invalid choice' | head -3
```

## Tema
Bounce: CLI legado + subcomandos
