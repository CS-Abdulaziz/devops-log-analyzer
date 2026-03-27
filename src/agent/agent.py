from .prompts import build_prompt
from .parser import parse_response
from .schema import IncidentResult


def analyze_log(user_input: str) -> IncidentResult:
    prompt = build_prompt(user_input)

# TODO: Integrate the actual model call from llm_setup.py
    response = ""

    return parse_response(response)