from langgraph.types import Command

import uuid
import aiosqlite
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from .graph import builder
from config import *

class AgentBuilder:
    def __init__(
        self,
        planner_provider="openai",
        planner_model="o3-mini",
        writer_provider="openai",
        writer_model="gpt-4.1-nano",
        save_history="disabled",
        max_tokens=32768,
    ):
        self.planner_provider = planner_provider
        self.planner_model = planner_model
        self.writer_provider = writer_provider
        self.writer_model = writer_model
        self.save_history = save_history
        self.max_tokens = max_tokens
        self.thread_id = str(uuid.uuid4())

        self.thread = {
            "configurable": {
                "thread_id": self.thread_id,
                "planner_provider": self.planner_provider,
                "planner_model": self.planner_model,
                "writer_provider": self.writer_provider,
                "writer_model": self.writer_model,
                "max_tokens": self.max_tokens,
            }
        }

        # Setup graph/checkpointer once
        if self.save_history == "disabled":
            self.memory = MemorySaver()
            self.graph = builder.compile(checkpointer=self.memory)
        else:
            # For sqlite, connection is async so setup graph in methods instead
            self.memory = None
            self.graph = None

    async def run_graph(self, query: str = "What is Sakura?"):
        events = {"query": query}
        thread = {"configurable": {"thread_id": self.thread_id}}
        if self.save_history == "disabled":
            async for event in self.graph.astream(events, thread, stream_mode="updates"):
                # print("========================")
                # print(type(event))
                # print(event)
                if '__interrupt__' in event:
                    interrupt_value = event['__interrupt__'][0].value
                    return interrupt_value, False
        else:
            os.makedirs(APP_PATH_HISTORY, exist_ok=True)
            async with aiosqlite.connect(os.path.join(APP_PATH_HISTORY, "checkpoints_async.sqlite")) as conn:
                memory = AsyncSqliteSaver(conn)
                graph = builder.compile(checkpointer=memory)
                async for event in graph.astream(events, thread, stream_mode="updates"):
                    # print("========================")
                    # print(type(event))
                    # print(event)
                    if '__interrupt__' in event:
                        interrupt_value = event['__interrupt__'][0].value
                        return interrupt_value, False
                # final_state = graph.get_state(thread)
                final_state = await graph.aget_state(thread)
                final_output = final_state.values.get("conclusion")
                print(f"final_state: {final_state}")
                return final_output, True

        # final_state = self.graph.get_state(thread)


        # final_output = final_state.values.get("conclusion")


    async def resume_graph(self, resume: str):
        thread = {"configurable": {"thread_id": self.thread_id}}
        if self.save_history == "disabled":
            async for event in self.graph.astream(Command(resume=resume), thread, stream_mode="updates"):
                # print("========================")
                # print(type(event))
                # print(event)
                if '__interrupt__' in event:
                    interrupt_value = event['__interrupt__'][0].value
                    return interrupt_value, False
        else:
            async with aiosqlite.connect(os.path.join(APP_PATH_HISTORY, "checkpoints_async.sqlite")) as conn:
                memory = AsyncSqliteSaver(conn)
                graph = builder.compile(checkpointer=memory)
                async for event in graph.astream(Command(resume=resume), thread, stream_mode="updates"):
                    print("========================")
                    print(type(event))
                    print(event)
                    if '__interrupt__' in event:
                        interrupt_value = event['__interrupt__'][0].value
                        return interrupt_value, False
                # final_state = graph.get_state(thread)
                final_state = await graph.aget_state(thread)
                print(f"final_state: {final_state}")
                final_output = final_state.values.get("conclusion")
                return final_output, True

        final_state = self.graph.get_state(thread)
        final_output = final_state.values.get("conclusion")
        return final_output, True





    # async def run(self, file_path: str):
    #     """
    #     Run the graph asynchronously for a given input file.
    #     """
    #     event = {"orig_file_path": file_path}
    #     results = []
    #
    #     async for s in self.graph.astream(event, self.thread, stream_mode="updates"):
    #         # print("================================")
    #         # print(s)
    #         print("running...")
    #         results.append(s)
    #
    #     return results[-1]['response2file']["tool_save_path"]


# if __name__ == "__main__":
#     import asyncio
#     from dotenv import load_dotenv
#
#     load_dotenv()
#
#     file_path = ""
#
#     agent = AgentBuilder()
#     results = asyncio.run(agent.run(file_path))
