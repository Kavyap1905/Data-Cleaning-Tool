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
You are a senior data reliability engineer.

Generate ONLY executable Python pandas code to repair the dataframe.

STRICT RULES:
- Output MUST contain only raw Python code.
- Start immediately with imports.
- No explanation or markdown.
- Operate ONLY on existing dataframe variable: df.
- Do NOT read or write files.
- Do NOT print anything.
- Do NOT create new datasets.
- Do NOT drop rows unless absolutely necessary.
- Prefer fixing over deleting data.

DATA HEALING REQUIREMENTS:
1. Fix missing values appropriately:
   - numeric → median
   - categorical → mode or 'Unknown'
2. Correct data types where inconsistent.
3. Detect and treat outliers using IQR method and CLIP values (do NOT remove rows).
4. Remove duplicate rows safely.
5. Ensure schema consistency.
6. Never compute statistics on non-numeric columns.
7. Treat object/string columns as categorical.
8. Keep row count stable whenever possible.

Issues detected:
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

