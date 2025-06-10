from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt

from configuration import Configuration
from .state import *

def human_review(state: SectionState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    human_reviews = interrupt("What is your opinion?")
    return {"conclusion": human_reviews}

builder = StateGraph(SectionState, input=SectionInput, output=SectionOutput, config_schema=Configuration)
builder.add_node("human_review", human_review)

builder.add_edge(START, "human_review")
builder.add_edge("human_review", END)

graph = builder.compile()