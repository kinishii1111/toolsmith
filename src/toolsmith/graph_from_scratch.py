"""F1b — grafo from_scratch mínimo: 1 nó que lê/escreve `messages` via StateGraph.

Sem tools reais ainda. Se GROQ_API_KEY estiver no ambiente, usa ChatGroq;
senão, nó `reply` devolve mensagem fixa/eco da pergunta — o importante é provar
o StateGraph compilado e invocado (não print solto).
"""

import os

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph

from toolsmith.state import AgentState


def _make_reply_node():
    """Retorna nó `reply`. Prefere ChatGroq se houver chave; senão eco."""
    key = os.getenv("GROQ_API_KEY")
    if key:
        try:
            from langchain_groq import ChatGroq

            llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=key)

            def reply(state: AgentState) -> AgentState:
                last = state["messages"][-1].content
                return {"messages": [AIMessage(content=llm.invoke(last).content)]}

            return reply
        except Exception:
            pass

    def reply(state: AgentState) -> AgentState:
        last = state["messages"][-1].content
        return {"messages": [AIMessage(content=f"eco (F1b, sem tools): {last}")]}

    return reply


def build_graph():
    """StateGraph(AgentState) com 1 nó `reply` → compile()."""
    graph = StateGraph(AgentState)
    graph.add_node("reply", _make_reply_node())
    graph.set_entry_point("reply")
    graph.add_edge("reply", "__end__")
    return graph.compile()
