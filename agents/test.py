def test_agent(state):
    import pandas as pd

    df = state["data"]

    # -------------------------
    # Missing values
    # -------------------------
    missing_values = df.isnull().sum().to_dict()

    # -------------------------
    # Duplicate rows
    # -------------------------
    duplicates = int(df.duplicated().sum())

    # -------------------------
    # Data types
    # -------------------------
    dtypes = df.dtypes.astype(str).to_dict()

    # -------------------------
    # Outlier Detection (IQR)
    # -------------------------
    outliers = {}

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers[col] = int(
            ((df[col] < lower) | (df[col] > upper)).sum()
        )

    # -------------------------
    # Test Summary
    # -------------------------
    tests = {
        "missing_values_after": missing_values,
        "duplicates": duplicates,
        "outliers": outliers,
        "dtypes": dtypes,
        "row_count": len(df)
    }

    return {
        **state,
        "test_results": tests
    }
