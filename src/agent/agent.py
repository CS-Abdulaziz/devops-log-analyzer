from .parser import parse_response
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_setup import get_generator_model
from .schema import IncidentResult
from .prompts import SYSTEM_PROMPT


def analyze_log(log: str) -> IncidentResult:
    model = get_generator_model()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=log)
    ]

    response = model.invoke(messages)

    return parse_response(response.content)