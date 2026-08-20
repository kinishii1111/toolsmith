"""F3a — tool local de rascunho de resposta (template, sem LLM)."""

from langchain_core.tools import tool


@tool
def draft_reply(contexto: str, tom: str = "objetivo") -> str:
    """Gera rascunho de resposta ao cliente a partir do contexto.

    `contexto` deve trazer classificação + trechos da KB. `tom`: objetivo|empático.
    Local, sem LLM — template string.
    """
    tom = tom.lower().strip()
    if tom not in ("objetivo", "empatico", "empático"):
        tom = "objetivo"
    saudacao = "Olá! Entendo a situação" if "empat" in tom else "Olá,"
    return (
        f"{saudacao}\n\n"
        f"Contexto analisado: {contexto[:800]}\n\n"
        "Encaminhamento sugerido:\n"
        "1) Tente os passos da KB (limpar cache/aba anônima e redefinir senha se for login).\n"
        "2) Se persistir, informe horário, navegador e print do erro para escalarmos.\n"
        "3) Severidade alta → SLA até 4h úteis.\n\n"
        f"Tom: {tom} | Time de suporte — Plantão chamado"
    )
