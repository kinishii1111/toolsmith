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
from toolsmith.tools.pesquisa import format_brief, web_search

TOOLS = [web_search, format_brief]

SYSTEM_PROMPT = (
    "Plantão pesquisa — não invente fatos. Use as tools web_search/format_brief "
    "para levantar informação e responda citando as URLs (http/https) que as tools "
    "retornarem. Fonte vazia/stub deixa claro que a busca não trouxe resultado."
)


def _make_agent_node():
    """Retorna nó `agent`. Prefere ChatGroq bind tools; senão eco (F2a sem key)."""
    key = os.getenv("GROQ_API_KEY")
    if key:
        try:
            from langchain_groq import ChatGroq

            llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=key).bind_tools(TOOLS)

            def agent(state: AgentState) -> AgentState:
                msgs = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
                return {"messages": [llm.invoke(msgs)]}

            return agent
        except Exception:
            pass

    def agent(state: AgentState) -> AgentState:
        last = state["messages"][-1].content
        return {
            "messages": [
                AIMessage(content=f"eco (F2a, sem GROQ_API_KEY — tools não chamadas): {last}")
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


def build_graph():
    """StateGraph(AgentState): agent → (tools | end) → tools → agent."""
    graph = StateGraph(AgentState)
    graph.add_node("agent", _make_agent_node())
    graph.add_node("tools", ToolNode(TOOLS))
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        _should_continue,
        {"continue": "tools", "end": "__end__"},
    )
    graph.add_edge("tools", "agent")
    return graph.compile()
