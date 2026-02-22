import duckdb
import pandas as pd

class SQLExecutor:
    """
    Executes SQL safely using DuckDB
    """

    def __init__(self):
        self.con = duckdb.connect(database=":memory:")

    def register_df(self, df: pd.DataFrame, table_name="data"):
        self.con.register(table_name, df)

    def execute(self, sql: str):
        """
        Executes SQL and returns dataframe
        """
        try:
            result = self.con.execute(sql).df()
            return {
                "success": True,
                "data": result,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }
