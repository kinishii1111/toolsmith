"""F3a — tool local de busca na KB markdown."""

from pathlib import Path

from langchain_core.tools import tool

KB_DIR = Path(__file__).parent / "kb"


@tool
def search_kb(query: str) -> str:
    """Busca trechos na KB local (kb/*.md) por palavras-chave.

    Retorna até 3 trechos relevantes (título + trecho). Sem RAG vetorial.
    """
    if not KB_DIR.exists():
        return "[search_kb] kb/ não encontrada"
    termos = [w.lower() for w in query.split() if len(w) >= 3]
    hits: list[str] = []
    for md in sorted(KB_DIR.glob("*.md")):
        try:
            txt = md.read_text(encoding="utf-8")
        except Exception:
            continue
        low = txt.lower()
        if any(t in low for t in termos) or query.lower() in low:
            # trecho: primeiras 600 chars
            trecho = txt.strip()[:600].replace("\n\n", "\n")
            hits.append(f"## {md.name}\n{trecho}")
        if len(hits) >= 3:
            break
    if not hits:
        # fallback: lista arquivos disponíveis
        disponiveis = ", ".join(p.name for p in KB_DIR.glob("*.md"))
        return f"[search_kb] sem match direto para: {query} | KB disponível: {disponiveis}"
    return "\n\n---\n\n".join(hits)
