"""Nó de resumo de histórico — F1.

Padrão LangGraph: se len(messages) > N, compactar antigas em `summary`
e manter as K últimas intactas. Sem LLM quando GROQ_API_KEY ausente.
"""

from __future__ import annotations

import os

SUMMARIZE_AFTER = 12
KEEP_LAST = 4

_TRUNCATE_AT = 2000


def should_summarize(state: dict) -> bool:
    """Retorna True quando há mensagens suficientes para compactar."""
    messages = state.get("messages") or []
    return len(messages) > SUMMARIZE_AFTER


def _content_to_str(m) -> str:
    c = getattr(m, "content", None)
    if isinstance(c, str):
        return c.strip()
    if isinstance(c, list):
        parts: list[str] = []
        for block in c:
            if isinstance(block, str):
                parts.append(block.strip())
            elif isinstance(block, dict) and "text" in block:
                v = block.get("text")
                if isinstance(v, str):
                    parts.append(v.strip())
        return " ".join(p for p in parts if p)
    return ""


def _build_fallback_summary(old_messages: list) -> str:
    parts = [_content_to_str(m) for m in old_messages]
    parts = [p for p in parts if p]
    raw = "\n".join(parts)
    if len(raw) > _TRUNCATE_AT:
        raw = raw[:_TRUNCATE_AT].rstrip() + "..."
    return raw


def summarize_node(state: dict) -> dict:
    """Nó puro: compacta mensagens antigas em `summary` e mantém as K últimas.

    Retorna dict com `summary` e `messages` (encurtado). Não importa graph_*.py.
    Sem GROQ_API_KEY usa junção truncada; com key tenta 1 call ChatGroq
    modelo `openai/gpt-oss-20b`.
    """
    messages: list = state.get("messages") or []
    existing_summary: str = state.get("summary") or ""

    if not messages:
        return {"summary": existing_summary, "messages": messages}

    if len(messages) <= KEEP_LAST:
        keep = messages
        old: list = []
    else:
        old = messages[:-KEEP_LAST]
        keep = messages[-KEEP_LAST:]

    if not old:
        return {"summary": existing_summary, "messages": keep}

    fallback = _build_fallback_summary(old)

    new_summary_text = fallback

    api_key = os.getenv("GROQ_API_KEY")
    if api_key and fallback:
        try:
            from langchain_groq import ChatGroq

            llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
            prompt = (
                "Resuma de forma concisa o histórico abaixo, preservando fatos, "
                "nomes e decisões. Não invente informação.\n\n"
                f"{fallback}"
            )
            resp = llm.invoke(prompt)
            content = getattr(resp, "content", None)
            if isinstance(content, str) and content.strip():
                new_summary_text = content.strip()
            elif isinstance(content, list):
                txt = _content_to_str(resp)
                if txt:
                    new_summary_text = txt
        except Exception:
            # Falha do id/modelo ou rede: mantém fallback truncado.
            # Não tenta id morto tipo llama-3.3-70b-versatile.
            new_summary_text = fallback

    if existing_summary and new_summary_text:
        combined = f"{existing_summary.strip()}\n{new_summary_text.strip()}"
    elif new_summary_text:
        combined = new_summary_text.strip()
    else:
        combined = existing_summary.strip()

    if len(combined) > _TRUNCATE_AT * 2:
        combined = combined[: _TRUNCATE_AT * 2].rstrip() + "..."

    return {"summary": combined, "messages": keep}
