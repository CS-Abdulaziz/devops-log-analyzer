import json
from .schema import IncidentResult


def parse_response(data) -> IncidentResult:

    try:
        if isinstance(data, str):
            data = json.loads(data)

        fixes = data.get("suggested_fixes", [])
        if isinstance(fixes, str):
            fixes = [fixes]
        elif not isinstance(fixes, list):
            fixes = ["No fix provided"]

        confidence = data.get("confidence", 0)

        if isinstance(confidence, float) and confidence <= 1:
            confidence = int(confidence * 100)
        elif isinstance(confidence, (int, float)):
            confidence = int(confidence)
        else:
            confidence = 0


        return IncidentResult(
            
            issue_type=data.get("issue_type", "Unknown"),
            root_cause=data.get("root_cause", "Unknown"),
            suggested_fixes=fixes,
            confidence=confidence,
        )

    except Exception:
        return IncidentResult(
            issue_type="Parsing Error",
            root_cause="Could not parse model response",
            suggested_fixes=["Check model output format"],
            confidence=0,
        )