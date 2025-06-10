import asyncio
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph

async def main():
    # 1. Build a simple graph (add_one node)
    builder = StateGraph(int)
    builder.add_node("add_one", lambda x: x + 1)
    builder.set_entry_point("add_one")
    builder.set_finish_point("add_one")

    # 2. Open an aiosqlite async connection
    #    - "checkpoints_async.sqlite" is the file where checkpoints are stored
    async with aiosqlite.connect("checkpoints_async.sqlite") as conn:
        # 3. Create the AsyncSqliteSaver using the async connection
        saver = AsyncSqliteSaver(conn)

        # 4. Compile the graph with async checkpointer
        graph = builder.compile(checkpointer=saver)

        # 5. Provide a config (unique thread_id)
        config = {"configurable": {"thread_id": "async-1"}}

        # 6. (Optional) Inspect initial state (must use 'await' for async methods)
        state = await graph.ainvoke(3, config)
        print("Result after async invoke:", state)

        # 7. (Optional) Get current state snapshot
        snapshot = await graph.aget_state(config)
        print("Async state snapshot:", snapshot)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
