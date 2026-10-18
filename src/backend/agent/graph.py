from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class EchoState(TypedDict):
    text: str
    reply: str


def _echo(state: EchoState) -> dict[str, str]:
    return {"reply": state["text"]}


def build_echo_graph():
    builder = StateGraph(EchoState)
    builder.add_node("echo", _echo)
    builder.add_edge(START, "echo")
    builder.add_edge("echo", END)
    return builder.compile()
