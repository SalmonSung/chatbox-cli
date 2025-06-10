import uuid
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from .graph import builder

async def simple_wrapper():
    event = {"query": "What is Sakura?"}
    results = []
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    thread = {
            "configurable": {
                "thread_id": str(uuid.uuid4()),
            }
        }
    async for s in graph.astream(event, thread, stream_mode="updates"):
        # print("================================")
        # print(s)
        print("running...")
        results.append(s)
    return results[-1]

async def run_graph():
    events = {"query": "What is Sakura?"}
    results = []
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    thread = {
            "configurable": {
                # "thread_id": str(uuid.uuid4()),
                "thread_id": "ABCD1234ABCD1234",
            }

        }
    async for event in graph.astream(events, thread, stream_mode="updates"):
        print("========================")
        print(type(event))
        print(event)
        if '__interrupt__' in event:
            interrupt_value = event['__interrupt__'][0].value
            return interrupt_value

async def resume_graph(resume: str):

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    thread = {
        "configurable": {
            # "thread_id": str(uuid.uuid4()),
            "thread_id": "ABCD1234ABCD1234",
        }

    }
    async for event in graph.astream(
            Command(resume=resume),
            thread, stream_mode="updates"):
        print("========================")
        print(type(event))
        print(event)
        if '__interrupt__' in event:
            interrupt_value = event['__interrupt__'][0].value
            return interrupt_value