from .schema import IncidentResult


def parse_response(data: dict) -> IncidentResult:
    try:
        return IncidentResult(
            issue_type=data.get("category", "Unknown"),
            root_cause=data.get("root_cause", "Unknown"),
            suggested_fixes=[data.get("fix", "No fix provided")],
            confidence=int(float(data.get("confidence", 0)) * 100)
            if data.get("confidence") is not None
            else 0,
        )

    except Exception:
        return IncidentResult(
            issue_type="Parsing Error",
            root_cause="Could not parse model response",
            suggested_fixes=["Check model output format"],
            confidence=0,
        )