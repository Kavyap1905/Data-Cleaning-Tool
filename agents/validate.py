from tools.schema_tools import infer_schema, detect_schema_drift

# imagine this is loaded from metadata store
STORED_SCHEMA = None

def validate_agent(state):
    df = state["data"]

    current_schema = infer_schema(df)

    drift = {}
    if STORED_SCHEMA:
        drift = detect_schema_drift(STORED_SCHEMA, df)

    report = {
        "schema": current_schema,
        "schema_drift": drift,
        "missing_values": df.isnull().sum().to_dict()
    }

    return {
        **state,
        "report": report
    }
