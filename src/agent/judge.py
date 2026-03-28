from langchain_core.messages import HumanMessage, SystemMessage
from langchain_setup import get_judge_model
import json
import re


JUDGE_PROMPT = """
You are an expert DevOps evaluator.

Evaluate:
1. Root cause accuracy (0-10)
2. Fix relevance (0-10)
3. Classification correctness (0-10)

Return ONLY JSON:
{
  "score": int,
  "feedback": "short explanation"
}
"""

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group()
    return None

def judge_response(log, result):
    model = get_judge_model()

    messages = [
        SystemMessage(content=JUDGE_PROMPT),
        HumanMessage(content=f"""
LOG:
{log}

MODEL OUTPUT:
{json.dumps(result, indent=2)}
""")
    ]

    response = model.invoke(messages)
    raw = response.content
    json_str = extract_json(raw)

    if json_str:
        return json.loads(json_str)
    else:
        return {
            "score": 0,
            "feedback": "Failed to parse judge response"
    }