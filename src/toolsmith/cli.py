import argparse
import os
import sys
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage

from toolsmith.graph_from_scratch import build_graph


def _load_env() -> None:
    """Carrega `.env` na raiz do pacote/repo se existir (POC)."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    # repo root: …/toolsmith/.env (pai de src/)
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env")


def _sem_key() -> None:
    print(
        "toolsmith: exige GROQ_API_KEY no ambiente (ver .env / README). "
        "Defina GROQ_API_KEY e rode de novo.",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> None:
    _load_env()
    parser = argparse.ArgumentParser(prog="toolsmith")
    parser.add_argument(
        "--cenario",
        choices=["pesquisa", "chamado", "lead"],
        default="pesquisa",
        help="cenário: pesquisa | chamado | lead (default: pesquisa)",
    )
    parser.add_argument(
        "pergunta",
        nargs="?",
        default="ping",
        help="pergunta opcional (default: ping)",
    )
    args = parser.parse_args()

    if not os.getenv("GROQ_API_KEY"):
        _sem_key()

    graph = build_graph(cenario=args.cenario)
    result = graph.invoke(
        {"messages": [HumanMessage(content=args.pergunta)]},
        config={"recursion_limit": 20},
    )

    # resposta final = última AIMessage sem tool_calls
    final = next(
        (m.content for m in reversed(result["messages"]) if isinstance(m, AIMessage) and not m.tool_calls),
        result["messages"][-1].content,
    )
    print(final)


if __name__ == "__main__":
    main()
