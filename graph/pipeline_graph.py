from langgraph.graph import StateGraph
from typing import TypedDict, Any
import pandas as pd
from agents.ingest import ingest_agent
from agents.validate import validate_agent
from agents.diagnose import diagnose_agent
from agents.fix import fix_agent
from agents.test import test_agent
from agents.approve import approve_agent

class PipelineState(TypedDict):
    data: pd.DataFrame
    report: dict
    fix_code: str
    test_results: dict
    approved: bool



def build_graph():
    graph = StateGraph(dict)

    graph.add_node("ingest", ingest_agent)
    graph.add_node("validate", validate_agent)
    graph.add_node("diagnose", diagnose_agent)
    graph.add_node("fix", fix_agent)
    graph.add_node("test", test_agent)
    graph.add_node("approve", approve_agent)

    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "validate")
    graph.add_edge("validate", "diagnose")
    graph.add_edge("diagnose", "fix")
    graph.add_edge("fix", "test")
    graph.add_edge("test", "approve")

    return graph.compile()
