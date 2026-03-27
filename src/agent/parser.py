import json
from .schema import IncidentResult


def parse_response(response: str) -> IncidentResult:
    try:
        data = json.loads(response)

        return IncidentResult(
            issue_type=data.get("issue_type", "Unknown"),
            root_cause=data.get("root_cause", "Unknown"),
            suggested_fixes=data.get("suggested_fixes", []),
            confidence=data.get("confidence", 50),
        )
    except Exception:
        return IncidentResult(
            issue_type="Parsing Error",
            root_cause="Could not parse model response",
            suggested_fixes=["Check model output format"],
            confidence=0,
        )