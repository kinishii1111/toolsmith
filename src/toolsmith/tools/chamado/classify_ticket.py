"""F3a — tool local de classificação de ticket (heurística)."""

from langchain_core.tools import tool


@tool
def classify_ticket(texto: str) -> str:
    """Classifica ticket por severidade e categoria (heurística local).

    Usa palavras-chave — sem LLM. Retorna severidade (alta/media/baixa)
    e categoria (login/senha/disponibilidade/geral).
    """
    t = texto.lower()
    severidade = "baixa"
    if any(k in t for k in ["pressa", "urgente", "critico", "crítico", "desde ontem", "desde hoje", "nao funciona", "não funciona", "fora do ar", "parado", "bloqueado", "erro 500"]):
        severidade = "alta"
    elif any(k in t for k in ["lento", "demora", "intermitente", "as vezes", "às vezes"]):
        severidade = "média"

    if any(k in t for k in ["login", "logar", "acesso", "autentic"]):
        categoria = "login"
    elif any(k in t for k in ["senha", "bloqueio", "credenciais"]):
        categoria = "senha"
    elif any(k in t for k in ["fora do ar", "lento", "500", "disponibilidade", "instavel", "instável"]):
        categoria = "disponibilidade"
    else:
        categoria = "geral"

    return f"Severidade: {severidade} | Categoria: {categoria} | Texto: {texto[:200]}"
