import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="toolsmith")
    parser.add_argument(
        "--cenario",
        choices=["pesquisa", "chamado", "lead"],
        default="pesquisa",
        help="cenário: pesquisa | chamado | lead (default: pesquisa)",
    )
    args = parser.parse_args()
    print(f"ToolSmith F0 ok [{args.cenario}]")


if __name__ == "__main__":
    main()
