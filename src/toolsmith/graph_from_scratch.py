"""F2a — grafo from_scratch ReAct com loop tool (llm ↔ tools).

Nós: `agent` (LLM bind tools) → condicional `should_continue` → `tools`
(ToolNode) → volta pro `agent`. Prefere ChatGroq + ToolNode se GROQ_API_KEY
existir; senão modo degradado: nó `agent` ecoa a pergunta (sem chamar tools),
documentado no README — o grafo continua compilando e rodando.
"""

import os

from langchain_core.messages import AIMessage, SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from toolsmith.state import AgentState
from toolsmith.tools.chamado import classify_ticket, draft_reply, search_kb
from toolsmith.tools.pesquisa import format_brief, web_search

TOOLS_PESQUISA = [web_search, format_brief]
TOOLS_CHAMADO = [classify_ticket, search_kb, draft_reply]
# compat: F2 usava TOOLS
TOOLS = TOOLS_PESQUISA

SYSTEM_PROMPT_PESQUISA = (
    "Plantão pesquisa — não invente fatos. Use as tools web_search/format_brief "
    "para levantar informação e responda citando as URLs (http/https) que as tools "
    "retornarem. Fonte vazia/stub deixa claro que a busca não trouxe resultado."
)
SYSTEM_PROMPT_CHAMADO = (
    "Plantão chamado — não invente; use tools. Pipeline obrigatório: classify_ticket para severidade/categoria, "
    "search_kb para trechos da KB em kb/*.md, draft_reply para rascunhar resposta. "
    "Na resposta final mencione severidade, cite o trecho/arquivo da KB usado e traga o rascunho. "
    "Termine obrigatoriamente com linha final `ESCALAR: sim|nao — motivo` "
    "(ex: `ESCALAR: sim — alta+sem reset ha >24h, exige N2` ou `ESCALAR: nao — contornável via KB`). "
    "Sem match na KB, diga que não há trecho direto."
)
# compat
SYSTEM_PROMPT = SYSTEM_PROMPT_PESQUISA


def _get_tools_and_prompt(cenario: str):
    c = (cenario or "pesquisa").lower()
    if c == "chamado":
        return TOOLS_CHAMADO, SYSTEM_PROMPT_CHAMADO
    return TOOLS_PESQUISA, SYSTEM_PROMPT_PESQUISA


def _make_agent_node(cenario: str = "pesquisa"):
    """Retorna nó `agent`. Prefere ChatGroq bind tools; senão eco (sem key)."""
    tools, prompt = _get_tools_and_prompt(cenario)
    key = os.getenv("GROQ_API_KEY")
    if key:
        try:
            from langchain_groq import ChatGroq

            llm = ChatGroq(model="openai/gpt-oss-20b", api_key=key).bind_tools(tools)

            def agent(state: AgentState) -> AgentState:
                msgs = [SystemMessage(content=prompt)] + state["messages"]
                return {"messages": [llm.invoke(msgs)]}

            return agent
        except Exception:
            pass

    def agent(state: AgentState) -> AgentState:
        last = state["messages"][-1].content
        return {
            "messages": [
                AIMessage(content=f"eco (sem GROQ_API_KEY — tools não chamadas): {last}")
            ]
        }

    return agent


def _should_continue(state: AgentState) -> str:
    """tools_condition: se o último AIMessage pediu tool, vai pra tools; senão fim."""
    messages = state["messages"]
    last = messages[-1]
    if not last.tool_calls:
        return "end"
    return "continue"


def build_graph(cenario: str = "pesquisa"):
    """StateGraph(AgentState): agent → (tools | end) → tools → agent.

    Seleciona TOOLS + prompt conforme `cenario` (pesquisa|chamado).
    """
    tools, _ = _get_tools_and_prompt(cenario)
    graph = StateGraph(AgentState)
    graph.add_node("agent", _make_agent_node(cenario))
    graph.add_node("tools", ToolNode(tools))
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        _should_continue,
        {"continue": "tools", "end": "__end__"},
    )
    graph.add_edge("tools", "agent")
    return graph.compile()
