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

from toolsmith.memory import get_checkpointer
from toolsmith.state import AgentState
from toolsmith.summarize import should_summarize, summarize_node
from toolsmith.tools.chamado import classify_ticket, draft_reply, search_kb
from toolsmith.tools.lead import draft_lead_reply, score_lead, tag_lead
from toolsmith.tools.pesquisa import format_brief, web_search

TOOLS_PESQUISA = [web_search, format_brief]
TOOLS_CHAMADO = [classify_ticket, search_kb, draft_reply]
TOOLS_LEAD = [score_lead, tag_lead, draft_lead_reply]
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
SYSTEM_PROMPT_LEAD = (
    "Plantão lead — não invente; use tools. Pipeline obrigatório em 1 tacada: "
    "score_lead para 0–100 + motivos (ICP em tools/lead/regras.md: orçamento/urgência/segmento), "
    "tag_lead para quente|morno|frio e b2b|b2c, draft_lead_reply para rascunho WhatsApp/e-mail curto. "
    "Na resposta final traga rascunho útil (proposta/call) e termine obrigatoriamente com duas linhas finais: "
    "`SCORE: <0-100>` e `TAGS: quente|morno|frio, b2b|b2c` "
    "(ex: `SCORE: 85` + `TAGS: quente, b2b`). Ouro: msg crua → qualificado + resposta + tag."
)
# compat
SYSTEM_PROMPT = SYSTEM_PROMPT_PESQUISA


def _get_tools_and_prompt(cenario: str):
    c = (cenario or "pesquisa").lower()
    if c == "chamado":
        return TOOLS_CHAMADO, SYSTEM_PROMPT_CHAMADO
    if c == "lead":
        return TOOLS_LEAD, SYSTEM_PROMPT_LEAD
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


def _should_summarize(state: AgentState) -> str:
    """Condicional do entry: resume (summarize_node) ou vai direto pro agent."""
    return "summarize" if should_summarize(state) else "agent"


def build_graph(cenario: str = "pesquisa", checkpointer=None):
    """StateGraph(AgentState): summarize → agent → (tools | end) → tools → agent.

    Seleciona TOOLS + prompt conforme `cenario` (pesquisa|chamado|lead).
    `checkpointer` None ⇒ usa `get_checkpointer()` (SqliteSaver) para memória
    por thread_id. Nó `summarize` compacta histórico antes do agent quando
    `should_summarize` retornar True.
    """
    if checkpointer is None:
        checkpointer = get_checkpointer()
    tools, _ = _get_tools_and_prompt(cenario)
    graph = StateGraph(AgentState)
    graph.add_node("summarize", summarize_node)
    graph.add_node("agent", _make_agent_node(cenario))
    graph.add_node("tools", ToolNode(tools))
    graph.set_conditional_entry_point(
        _should_summarize,
        {"summarize": "summarize", "agent": "agent"},
    )
    graph.add_edge("summarize", "agent")
    graph.add_conditional_edges(
        "agent",
        _should_continue,
        {"continue": "tools", "end": "__end__"},
    )
    graph.add_edge("tools", "agent")
    return graph.compile(checkpointer=checkpointer)
