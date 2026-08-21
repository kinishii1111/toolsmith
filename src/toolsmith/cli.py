import argparse
import os
import sqlite3
import sys
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage

from toolsmith.graph_from_scratch import build_graph as build_scratch
from toolsmith.graph_prebuilt import build_graph as build_prebuilt
from toolsmith.memory import DEFAULT_DB, get_checkpointer


def _db_path() -> Path:
    """Path do sqlite: honra TOOLSMITH_CHECKPOINT, senão o DEFAULT_DB."""
    env = os.getenv("TOOLSMITH_CHECKPOINT")
    return Path(env) if env else DEFAULT_DB


def _load_env() -> None:
    """Carrega `.env` na raiz do pacote/repo se existir (POC)."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env")


def _sem_key() -> None:
    print(
        "toolsmith: exige GROQ_API_KEY no ambiente (ver .env / README). "
        "Defina GROQ_API_KEY e rode de novo.",
        file=sys.stderr,
    )
    sys.exit(1)


def _build_graph(motor: str, cenario: str) -> tuple:
    """Monta o grafo já compilado com o checkpointer do DB corrente."""
    db = _db_path()
    db.parent.mkdir(parents=True, exist_ok=True)
    checkpointer = get_checkpointer(db)
    if motor == "prebuilt":
        return build_prebuilt(cenario=cenario, checkpointer=checkpointer), checkpointer
    return build_scratch(cenario=cenario, checkpointer=checkpointer), checkpointer


def _list_threads(db: Path) -> list[str]:
    """Thread_ids distintos do sqlite de checkpoints."""
    if not db.exists():
        return []
    conn = sqlite3.connect(str(db))
    try:
        rows = conn.execute(
            "SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id"
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()
    return [r[0] for r in rows]


def _print_threads(db: Path) -> None:
    threads = _list_threads(db)
    if not threads:
        print("(sem threads ainda)")
        return
    for t in threads:
        print(t)


def _print_inspect(args) -> None:
    """`inspect THREAD`: último checkpoint (summary + últimas msgs resumidas)."""
    graph, checkpointer = _build_graph(args.motor, args.cenario)
    try:
        state = graph.get_state({"configurable": {"thread_id": args.thread}})
    finally:
        checkpointer.conn.close()
    if not state or not state.values or not state.values.get("messages"):
        print(f"thread '{args.thread}': sem checkpoint")
        return
    msgs = state.values["messages"]
    print(f"thread: {args.thread}  (último checkpoint)")
    summary = state.values.get("summary")
    if summary:
        print(f"summary: {summary}")
    for m in msgs[-4:]:
        role = m.__class__.__name__
        content = str(m.content).replace("\n", " ")[:160]
        print(f"- {role}: {content}")


def _final_answer(result) -> str:
    return next(
        (m.content for m in reversed(result["messages"]) if isinstance(m, AIMessage) and not m.tool_calls),
        result["messages"][-1].content,
    )


def _run_invoke(graph, thread: str, pergunta: str) -> None:
    config = {"configurable": {"thread_id": thread}, "recursion_limit": 20}
    result = graph.invoke(
        {"messages": [HumanMessage(content=pergunta)]},
        config=config,
    )
    print(_final_answer(result))


def _run_stream(graph, thread: str, pergunta: str) -> None:
    config = {"configurable": {"thread_id": thread}, "recursion_limit": 20}
    out = []
    for _chunk, _meta in graph.stream(
        {"messages": [HumanMessage(content=pergunta)]},
        config=config,
        stream_mode="messages",
    ):
        content = getattr(_chunk, "content", None)
        if isinstance(content, str) and content:
            out.append(content)
    print("".join(out) if out else _final_answer(graph.get_state(config).values))


_COMANDOS = {"threads", "inspect", "chat"}


def main() -> None:
    _load_env()
    argv = sys.argv[1:]
    if argv and argv[0] not in _COMANDOS and not argv[0].startswith("-"):
        sys.argv = [sys.argv[0], "chat", *argv]
    parser = argparse.ArgumentParser(prog="toolsmith")
    sub = parser.add_subparsers(dest="cmd", metavar="<comando>")

    sub.add_parser("threads", help="lista thread_ids do sqlite e sai")

    p_inspect = sub.add_parser("inspect", help="imprime último checkpoint da thread")
    p_inspect.add_argument("thread", help="thread_id a inspecionar")
    p_inspect.add_argument("--cenario", choices=["pesquisa", "chamado", "lead"], default="pesquisa")
    p_inspect.add_argument("--motor", choices=["scratch", "prebuilt"], default="scratch")

    p_chat = sub.add_parser(
        "chat", help="pergunta na thread (modo padrão)"
    )
    p_chat.add_argument("pergunta", nargs="?", default="ping")
    p_chat.add_argument("--thread", default="default", help="id de memória (default: default)")
    p_chat.add_argument(
        "--stream", action="store_true", help="força streaming token-a-token"
    )
    p_chat.add_argument("--cenario", choices=["pesquisa", "chamado", "lead"], default="pesquisa")
    p_chat.add_argument("--motor", choices=["scratch", "prebuilt"], default="scratch")

    # fallback: `toolsmith "pergunta" [--thread X]` sem subcomando
    parser.add_argument("pergunta_legada", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("--thread", dest="thread_legada", default="default", help=argparse.SUPPRESS)
    parser.add_argument("--stream", dest="stream_legada", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--cenario", dest="cenario_legada", default="pesquisa", help=argparse.SUPPRESS)
    parser.add_argument("--motor", dest="motor_legada", default="scratch", help=argparse.SUPPRESS)

    args = parser.parse_args()
    db = _db_path()

    if args.cmd == "threads":
        _print_threads(db)
        return

    if args.cmd == "inspect":
        _print_inspect(args)
        return

    # modo chat (subcomando ou legado sem subcomando)
    if args.cmd == "chat":
        pergunta = args.pergunta
        thread = args.thread
        stream = args.stream
        cenario = args.cenario
        motor = args.motor
    else:
        pergunta = args.pergunta_legada or "ping"
        thread = args.thread_legada
        stream = args.stream_legada
        cenario = args.cenario_legada
        motor = args.motor_legada

    if not os.getenv("GROQ_API_KEY"):
        _sem_key()

    graph, checkpointer = _build_graph(motor, cenario)
    try:
        if stream or sys.stdout.isatty():
            _run_stream(graph, thread, pergunta)
        else:
            _run_invoke(graph, thread, pergunta)
    finally:
        checkpointer.conn.close()


if __name__ == "__main__":
    main()
