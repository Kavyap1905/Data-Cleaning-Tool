def test_agent(state):
    df = state["data"]

    tests = {
        "missing_values_after": df.isnull().sum().to_dict(),
        "row_count": len(df)
    }

    return {
        **state,
        "test_results": tests
    }
