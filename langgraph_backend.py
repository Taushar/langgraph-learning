from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages


class chatstate(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


model = ChatOllama(model="qwen3:8b")


def chat_node(state: chatstate):
    messages = state["messages"]

    response = model.invoke(messages)

    return {"messages": [response]}


checkpointer = MemorySaver()
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

graph = StateGraph(chatstate)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)
