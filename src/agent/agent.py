from .parser import parse_response
from .schema import IncidentResult
from llm_setup import LogAnalyzer


analyzer = LogAnalyzer()


def analyze_log(user_input: str) -> IncidentResult:
    raw_result = analyzer.analyze_log(user_input)
    return parse_response(raw_result)