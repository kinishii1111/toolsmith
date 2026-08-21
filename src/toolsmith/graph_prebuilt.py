"""F5a — grafo prebuilt via `create_react_agent` (mesmos TOOLS/prompt do scratch).

Referência: https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/
Docs atuais `langgraph.prebuilt` (nome pode ser `create_react_agent`).
Reusa TOOLS/prompt de `graph_from_scratch` para comparar 1 motor em 2 jeitos.
Sem GROQ_API_KEY cai em fallback echo via StateGraph (sem traceback).
"""

import os

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph

from toolsmith.graph_from_scratch import _get_tools_and_prompt
from toolsmith.memory import get_checkpointer
from toolsmith.state import AgentState


def _echo_graph():
    """Fallback sem LLM: StateGraph com 1 nó echo (mesmo contrato do scratch)."""

    def reply(state: AgentState) -> AgentState:
        last = state["messages"][-1].content if state["messages"] else "ping"
        return {"messages": [AIMessage(content=f"eco (sem GROQ_API_KEY — prebuilt): {last}")]}

    g = StateGraph(AgentState)
    g.add_node("agent", reply)
    g.set_entry_point("agent")
    return g.compile()


def build_graph(cenario: str = "pesquisa", checkpointer=None):
    """Prebuilt `create_react_agent` com mesmos TOOLS/prompt do scratch.

    Seleciona kit por `cenario` (pesquisa|chamado|lead).
    `checkpointer` None ⇒ usa `get_checkpointer()` (SqliteSaver) para memória
    por thread_id. Obs: nó summarize só existe no scratch — o prebuilt não
    expõe hook fácil pra isso; aqui fica só memória via checkpointer.
    """
    if checkpointer is None:
        checkpointer = get_checkpointer()
    tools, prompt = _get_tools_and_prompt(cenario)
    key = os.getenv("GROQ_API_KEY")
    if key:
        try:
            from langchain_groq import ChatGroq
            from langgraph.prebuilt import create_react_agent

            model = ChatGroq(model="openai/gpt-oss-20b", api_key=key)
            # create_react_agent já cria loop agent→tools→agent
            return create_react_agent(
                model, tools, prompt=prompt, checkpointer=checkpointer
            )
        except Exception:
            pass
    return _echo_graph()
