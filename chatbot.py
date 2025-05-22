from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Define the state for the chatbot
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the graph
graph_builder = StateGraph(State)

# Set up the OpenAI LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# Define the chatbot node
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()

# Run the chatbot
while True:
    user_input = input(">> ")
    if user_input.lower() in ["quit", "exit"]:
        break
    state = {"messages": [{"role": "user", "content": user_input}]}
    for event in graph.stream(state):
        for value in event.values():
            print("Chatbot:", value["messages"][-1].content)
