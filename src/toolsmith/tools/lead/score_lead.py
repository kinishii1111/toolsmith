"""F4a — tool local de score de lead (heurística ICP)."""

import re

from langchain_core.tools import tool

# Regras ICP (espelho de regras.md) — dict local
ICP_REGRAS = {
    "orcamento_bonus": 30,
    "urgencia_bonus": 25,
    "segmento_b2b_bonus": 25,
    "base": 20,
}


@tool
def score_lead(texto: str) -> str:
    """Calcula score 0–100 + motivos (heurística local, sem LLM).

    Regras ICP (ver tools/lead/regras.md): orçamento explícito,
    urgência (essa semana/urgente/proposta) e segmento B2B (empresa/funcionarios).
    Retorna строка SCORE: N | motivos.
    """
    t = texto.lower()
    score = ICP_REGRAS["base"]
    motivos: list[str] = [f"base {ICP_REGRAS['base']}"]

    # Orçamento: até 20k, 20k, 20000, R$, orçamento
    if any(k in t for k in ["orcamento", "orçamento", "20k", "20000", "r$"]):
        # bônus maior se menciona 20k/20000
        if any(k in t for k in ["20k", "20000", "20 mil"]):
            score += 30
            motivos.append("orçamento até 20k explícito +30")
        else:
            score += 20
            motivos.append("orçamento mencionado +20")
    # alternativa: procura número com k
    elif re.search(r"\b\d+\s*k\b", t):
        score += 25
        motivos.append("valor em k mencionado +25")

    # Urgência
    if any(k in t for k in ["essa semana", "urgente", "imediato", "proposta", "preciso", "pra ontem", "o quanto antes"]):
        score += ICP_REGRAS["urgencia_bonus"]
        motivos.append("urgência/proposta essa semana +25")
    elif any(k in t for k in ["interesse", "quero saber", "avaliando"]):
        score += 10
        motivos.append("interesse moderado +10")

    # Segmento / tamanho
    if any(k in t for k in ["empresa", "funcionarios", "funcionários", "equipe", "cnpj", "b2b", "colaboradores"]):
        score += ICP_REGRAS["segmento_b2b_bonus"]
        motivos.append("segmento B2B/empresa +25")
        # bônus extra tamanho
        m = re.search(r"(\d+)\s*funcionarios", t) or re.search(r"(\d+)\s*funcionários", t)
        if m and int(m.group(1)) >= 20:
            score += 5
            motivos.append("porte >=20 funcionários +5")

    score = max(0, min(100, score))
    motivos_str = "; ".join(motivos)
    return f"SCORE: {score} | Motivos: {motivos_str} | Texto: {texto[:200]}"
