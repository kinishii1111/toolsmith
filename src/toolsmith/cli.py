import argparse

from langchain_core.messages import HumanMessage

from toolsmith.graph_from_scratch import build_graph


def main() -> None:
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

    graph = build_graph()
    result = graph.invoke({"messages": [HumanMessage(content=args.pergunta)]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
