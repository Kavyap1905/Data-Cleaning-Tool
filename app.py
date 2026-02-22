import streamlit as st
import pandas as pd
from graph.pipeline_graph import build_graph
from utils.safety import safe_execute

st.set_page_config("Self-Healing Data Pipeline", layout="wide")
st.title("🧠 Self-Healing Data Pipeline Agent")

uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.subheader("Original Data")
    st.dataframe(df)

    graph = build_graph()

    state = {"data": df}
    result = graph.invoke(state)

    fixed_df, error = safe_execute(df, result["fix_code"])

    st.subheader("Fix Code Generated")
    st.code(result["fix_code"], language="python")

    if error:
        st.error(f"Execution failed: {error}")
    else:
        st.subheader("Fixed Data")
        st.dataframe(fixed_df)

    st.subheader("Test Results")
    st.json(result["test_results"])

    st.subheader("Approval Status")
    st.success("Approved ✅" if result["approved"] else "Needs Review ❌")