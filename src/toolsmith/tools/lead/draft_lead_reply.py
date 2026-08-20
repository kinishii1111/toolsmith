"""F4a — tool local de rascunho WhatsApp/e-mail para lead."""

from langchain_core.tools import tool


@tool
def draft_lead_reply(texto: str, score: int = 50, tags: str = "morno, b2c") -> str:
    """Gera rascunho curto WhatsApp/e-mail a partir de texto + score + tags.

    Local, sem LLM — template. `texto` é a mensagem crua do lead.
    """
    try:
        sc = int(str(score).strip())
    except Exception:
        sc = 50
    tags = tags.lower().strip() if tags else "morno, b2c"
    # tom por temperatura
    if "quente" in tags:
        tom = "quente — priorize retorno hoje"
    elif "frio" in tags:
        tom = "frio — nutrir"
    else:
        tom = "morno — acompanhar"

    # snippet do lead
    snippet = texto[:300].strip()

    return (
        f"Olá! Obrigado pelo contato — recebemos: \"{snippet}\".\n\n"
        f"Perfil identificado: SCORE {sc} | TAGS {tags} ({tom}).\n"
        "Proposta: com esse porte/orçamento e urgência para essa semana, "
        "consigo te mandar uma proposta até 20k ainda hoje com escopo + prazo.\n"
        "Topa uma call de 15min hoje para alinharmos decisores e próximo passo?\n\n"
        f"Contexto: {snippet[:180]}\n"
        "— Plantão lead"
    )
