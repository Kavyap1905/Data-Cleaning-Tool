def approve_agent(state):
    tests = state["test_results"]

    approved = all(v == 0 for v in tests["missing_values_after"].values())

    return {
        **state,
        "approved": approved
    }
