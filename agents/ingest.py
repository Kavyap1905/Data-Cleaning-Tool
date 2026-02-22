
from tools.sql_executor import SQLExecutor

def ingest_agent(state):
    if state.get("source") == "sql":
        executor = SQLExecutor()
        executor.register_df(state["data"], "raw_data")

        result = executor.execute("SELECT * FROM raw_data")

        state["data"] = result["data"]

    return state
