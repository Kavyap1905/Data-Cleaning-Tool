import pandas as pd

def infer_schema(df: pd.DataFrame) -> dict:
    """
    Infer schema from dataframe
    """
    return {
        col: {
            "dtype": str(df[col].dtype),
            "nullable": df[col].isnull().any()
        }
        for col in df.columns
    }


def detect_schema_drift(old_schema: dict, new_df: pd.DataFrame) -> dict:
    """
    Detect schema drift between stored schema and new dataframe
    """
    drift = {
        "added_columns": [],
        "removed_columns": [],
        "type_changes": {}
    }

    new_schema = infer_schema(new_df)

    old_cols = set(old_schema.keys())
    new_cols = set(new_schema.keys())

    drift["added_columns"] = list(new_cols - old_cols)
    drift["removed_columns"] = list(old_cols - new_cols)

    for col in old_cols.intersection(new_cols):
        if old_schema[col]["dtype"] != new_schema[col]["dtype"]:
            drift["type_changes"][col] = {
                "old": old_schema[col]["dtype"],
                "new": new_schema[col]["dtype"]
            }

    return drift
