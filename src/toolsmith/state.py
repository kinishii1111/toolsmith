from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import NotRequired, TypedDict


class AgentState(TypedDict):
    """Estado compartilhado dos 3 cenários.

    Único state para pesquisa/chamado/lead; messages acumula via add_messages.
    """

    messages: Annotated[list, add_messages]
    summary: NotRequired[str]
