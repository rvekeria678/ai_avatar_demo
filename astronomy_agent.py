from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_tavily import TavilySearch

load_dotenv()
@tool
def search(query: str) -> list:
    """
    Searches a query through a search engine and returns the best results.
    Args:
        query: prompt used to search results
    """
    print("(Query Search Tool Invoked)")
    results = TavilySearch(max_results=2).invoke(query)
    return [result["content"] for result in results]

tools = [search]

llm = init_chat_model("gpt-3.5-turbo")
llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content="""
You are a helpful research assistant that can only answer questions about astronomy and nothing else. 

If you recieve a question that does not relate to astronomy, tell the user you can not answer that question.

Keep responses to less than 10 words. If not, respond with 'no comment.'

Only call the search tool if the user's question truly requires real-time information.

Once you have enough information, answer clearly and concisely and stop.

Avoid repeating tool calls unless the previous result was incomplete.
""")

# Node
def assistant(state: MessagesState):
    messages = [sys_msg] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": state["messages"] + [response]}

def route_assistant(state: MessagesState) -> str:
    last_message = state['messages'][-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    else:
        return END # No tool use, end the graph

# Build Graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.set_entry_point("assistant")

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", route_assistant)
builder.add_edge("tools", "assistant")
graph = builder.compile()

# Run
def astronomy_agent_response(query: str):
    initial_state = {"messages": HumanMessage(content=query)}
    final_state = graph.invoke(initial_state)

    ai_messages = []

    for msg in final_state["messages"]:
        if msg.type == "ai":
            ai_messages.append(msg)
    return ai_messages[-1].content