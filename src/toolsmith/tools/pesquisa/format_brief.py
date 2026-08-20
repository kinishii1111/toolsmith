"""F2a — tool local de formatação de brief (sem LLM obrigatório)."""

from langchain_core.tools import tool


@tool
def format_brief(titulo: str, bullets: list[str]) -> str:
    """Formata um brief de pesquisa: título + lista de bullets.

    Local, sem LLM — transforma dados crus (ex.: saída de web_search)
    em texto organizado pronto para o currículo/relatório.
    """
    if not bullets:
        return f"# {titulo}\n\n(sem bullets)"
    corpo = "\n".join(f"- {b}" for b in bullets)
    return f"# {titulo}\n\n{corpo}"
