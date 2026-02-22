from openai import OpenAI
from tools.pandas_executor import PandasExecutor
import os


# --------------------------------------
# LLM Setup (DeepSeek via OpenRouter)
# --------------------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def call_llm(prompt: str):

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content


# --------------------------------------
# Fix Agent
# --------------------------------------
def fix_agent(state):

    df = state["data"]
    diagnosis = state["report"]["diagnosis"]

    prompt = f"""
You are a senior data engineer.

Generate ONLY executable Python pandas code to fix the dataset.

STRICT RULES:
- Output MUST contain only raw Python code.
- Import all required libraries.
- Start directly with imports.
- NO explanation.
- NO markdown.
- FIRST character must be valid Python.
- Operate only on dataframe variable: df.
- Do NOT read/write files.
- Do NOT print.
- Never compute mean/median on non-numeric columns.
- Treat object/string columns as categorical.

Issues to fix:
{diagnosis}
"""

    # ---- Call DeepSeek LLM ----
    fix_code = call_llm(prompt)
    fix_code = str(fix_code).strip()

    # safety cleanup
    fix_code = (
        fix_code.replace("```python", "")
        .replace("```", "")
        .strip()
    )

    # ---- Execute Fix ----
    executor = PandasExecutor(df)
    result = executor.execute(fix_code)

    state["fix_code"] = fix_code
    state["data"] = result["data"]
    state["fix_success"] = result["success"]
    state["fix_error"] = result["error"]

    return state

