"""F4a — tool local de tags de lead (heurística)."""

import re

from langchain_core.tools import tool


@tool
def tag_lead(texto: str) -> str:
    """Gera tags quente|morno|frio e b2b|b2c (heurística local).

    Temperatura via score heurístico replicado; segmento via palavras-chave.
    Retorna TAGS: ...
    """
    t = texto.lower()
    # replica score simples para definir temperatura
    score = 20
    if any(k in t for k in ["orcamento", "orçamento", "20k", "20000", "r$"]) or re.search(r"\b\d+\s*k\b", t):
        score += 30 if any(k in t for k in ["20k", "20000"]) else 20
    if any(k in t for k in ["essa semana", "urgente", "imediato", "proposta", "preciso"]):
        score += 25
    if any(k in t for k in ["empresa", "funcionarios", "funcionários", "cnpj", "b2b"]):
        score += 25
        m = re.search(r"(\d+)\s*funcion", t)
        if m and int(m.group(1)) >= 20:
            score += 5
    score = max(0, min(100, score))

    if score >= 70:
        temp = "quente"
    elif score >= 40:
        temp = "morno"
    else:
        temp = "frio"

    # segmento
    tags_seg: list[str] = []
    if any(k in t for k in ["empresa", "funcionarios", "funcionários", "cnpj", "b2b", "colaboradores", "equipe"]):
        tags_seg.append("b2b")
    if any(k in t for k in ["pessoa física", "b2c", "para mim", "meu uso"]):
        tags_seg.append("b2c")
    if not tags_seg:
        # default: se menciona empresa → b2b, senão b2c (mas F4a pede ambos como opção)
        tags_seg.append("b2b" if "empresa" in t else "b2c")
        # se texto muito curto e sem empresa, mantém b2c; ouro da ORDEM espera b2b para "empresa de 50 funcionarios"

    tags = [temp] + tags_seg
    return f"TAGS: {', '.join(tags)} | score~{score} | Texto: {texto[:180]}"
