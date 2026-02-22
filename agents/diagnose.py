from openai import OpenAI
import os

# Replace Ollama with DeepSeek via OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def diagnose_agent(state):
    report = state["report"]

    prompt = f"""
    You are a data quality agent.
    Analyze this validation report and identify issues.

    Report:
    {report}

    Return JSON with:
    - issues
    - severity
    - fix_strategy
    """

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    diagnosis = response.choices[0].message.content

    state["report"]["diagnosis"] = diagnosis
    return state