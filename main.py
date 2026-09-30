# LangGraph Multi-Agent Travel Booking System
# main.py

import os
import operator
from typing import TypedDict, Annotated

import psycopg
import streamlit as st
from psycopg.rows import dict_row
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights


# ============================================================
# LOAD .ENV
# ============================================================

# Get the folder where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Explicitly load .env from that folder
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


# ============================================================
# GET ENVIRONMENT VARIABLES / STREAMLIT SECRETS
# ============================================================

def get_secret(key):
    """
    First read from environment variables (.env locally).
    If not found, read from Streamlit Cloud Secrets.
    """
    value = os.getenv(key)

    if value:
        return value

    try:
        return st.secrets.get(key)
    except Exception:
        return None


DATABASE_URL = get_secret("DATABASE_URL")
GROQ_API_KEY = get_secret("GROQ_API_KEY")
TAVILY_API_KEY = get_secret("TAVILY_API_KEY")


# ============================================================
# CHECK API KEYS
# ============================================================

print("Checking environment variables...")
print("Groq API key loaded:", bool(GROQ_API_KEY))
print("Tavily API key loaded:", bool(TAVILY_API_KEY))
print("Database URL loaded:", bool(DATABASE_URL))


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to your .env file or Streamlit Cloud Secrets."
    )

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is missing. "
        "Add it to your .env file or Streamlit Cloud Secrets."
    )

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is missing. "
        "Add it to your .env file or Streamlit Cloud Secrets."
    )


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY
)


# ============================================================
# STATE
# ============================================================

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int


# ============================================================
# FLIGHT AGENT
# ============================================================

def flight_agent(state: TravelState):
    query = state["user_query"]

    flight_data = search_flights(query)

    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(
                content="Flight results fetched"
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ============================================================
# HOTEL AGENT
# ============================================================

def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"

    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(
                content="Hotel information fetched"
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ============================================================
# ITINERARY AGENT
# ============================================================

def itinerary_agent(state: TravelState):
    prompt = f"""
Create a travel itinerary.

User Query:
{state['user_query']}

Flight Results:
{state['flight_results']}

Hotel Results:
{state['hotel_results']}
"""

    response = llm.invoke(
        [
            SystemMessage(
                content="You are an expert travel planner."
            ),
            HumanMessage(
                content=prompt
            )
        ]
    )

    return {
        "itinerary": response.content,
        "messages": [
            response
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ============================================================
# FINAL RESPONSE AGENT
# ============================================================

def final_agent(state: TravelState):
    final_prompt = f"""
Generate a final travel response for the user.

User Query:
{state['user_query']}

Flights:
{state['flight_results']}

Hotels:
{state['hotel_results']}

Itinerary:
{state['itinerary']}
"""

    response = llm.invoke(
        [
            HumanMessage(
                content=final_prompt
            )
        ]
    )

    return {
        "messages": [
            response
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ============================================================
# BUILD LANGGRAPH
# ============================================================

graph = StateGraph(TravelState)

graph.add_node(
    "flight_agent",
    flight_agent
)

graph.add_node(
    "hotel_agent",
    hotel_agent
)

graph.add_node(
    "itinerary_agent",
    itinerary_agent
)

graph.add_node(
    "final_agent",
    final_agent
)


# ============================================================
# GRAPH FLOW
# ============================================================

graph.add_edge(
    START,
    "flight_agent"
)

graph.add_edge(
    "flight_agent",
    "hotel_agent"
)

graph.add_edge(
    "hotel_agent",
    "itinerary_agent"
)

graph.add_edge(
    "itinerary_agent",
    "final_agent"
)

graph.add_edge(
    "final_agent",
    END
)


# ============================================================
# POSTGRES CHECKPOINTER
# ============================================================

# autocommit=True is important because LangGraph
# PostgreSQL migrations use CREATE INDEX CONCURRENTLY.

_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True,
    row_factory=dict_row
)

checkpointer = PostgresSaver(_conn)

# Create LangGraph checkpoint tables
checkpointer.setup()


# ============================================================
# COMPILE GRAPH
# ============================================================

app = graph.compile(
    checkpointer=checkpointer
)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("          AI TRAVEL AGENT")
    print("===================================\n")

    user_input = input(
        "Enter your travel request: "
    )

    config = {
        "configurable": {
            "thread_id": "user_dilpreet"
        }
    }

    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content=user_input
                )
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    print("\n===================================")
    print("          FINAL RESPONSE")
    print("===================================\n")

    # Print the final AI response
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage):
            print(msg.content)
            break