import copy
import ast
import pandas as pd
import re


class PandasExecutor:
    def __init__(self, df: pd.DataFrame):
        self.original_df = df
        self.df = copy.deepcopy(df)

    # --------------------------------------------------
    # Extract ONLY real python code from LLM output
    # --------------------------------------------------
    def _extract_code(self, text: str) -> str:
    # remove markdown fences
        text = re.sub(r"```python|```", "", text, flags=re.IGNORECASE)

        lines = text.splitlines()

        # drop everything before first real python statement
        start_idx = 0
        for i, line in enumerate(lines):
            if re.match(r"^\s*(import |from |df\[|df\s*=|def |class )", line):
                start_idx = i
                break

        code = "\n".join(lines[start_idx:])

        # remove non-ascii characters
        code = code.encode("ascii", "ignore").decode()

        return code.strip()


    # --------------------------------------------------
    # SAFE EXECUTION
    # --------------------------------------------------
    def execute(self, raw_code: str):
        code = self._extract_code(raw_code)

        if not code:
            return {
                "success": False,
                "data": self.original_df,
                "error": "No executable Python found in LLM output.",
                "executed_code": raw_code,
            }

        # AST syntax validation
        try:
            ast.parse(code)
        except SyntaxError as e:
            return {
                "success": False,
                "data": self.original_df,
                "error": f"Syntax error: {e}",
                "executed_code": code,
            }

        # sandbox env
        local_env = {
            "df": self.df,
            "pd": pd,
        }

        try:
            exec(code, {}, local_env)
            self.df = local_env.get("df", self.df)

            return {
                "success": True,
                "data": self.df,
                "error": None,
                "executed_code": code,
            }

        except Exception as e:
            return {
                "success": False,
                "data": self.original_df,
                "error": str(e),
                "executed_code": code,
            }
