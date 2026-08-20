"""F2a — tool de busca web barata via `ddgs` (DuckDuckGo).

Se a rede falhar no POC, devolve stub documentado em vez de estourar —
o nó de tool nunca derruba o grafo.
"""

from langchain_core.tools import tool


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Busca na web e devolve snippets (título + link + trecho).

    Usado para levantar fatos antes de responder (capital, definições,
    notícias). Devolve texto pronto para colar num brief.
    """
    try:
        from ddgs import DDGS
    except ImportError:
        return _stub(query, reason="ddgs não instalado")

    try:
        results = DDGS().text(query, max_results=max_results)
    except Exception as exc:  # rede/anti-bot
        return _stub(query, reason=f"busca falhou: {exc}")

    if not results:
        return _stub(query, reason="sem resultados")

    lines = [f"Resultados para: {query}", ""]
    for i, r in enumerate(results, 1):
        title = r.get("title", "").strip()
        href = r.get("href", "").strip()
        body = (r.get("body") or "").strip().replace("\n", " ")
        lines.append(f"{i}. {title}\n   {href}\n   {body}")
    return "\n".join(lines)


def _stub(query: str, reason: str) -> str:
    return (
        f"[web_search stub — {reason}] Busca por: {query}\n"
        "Modo degradado do POC F2a: sem resultados da rede. "
        "Ver `ddgs` instalado e rede disponível."
    )
