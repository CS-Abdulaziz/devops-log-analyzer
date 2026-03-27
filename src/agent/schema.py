from pydantic import BaseModel, Field
from typing import List


class IncidentResult(BaseModel):
    issue_type: str = Field(description="Short label of the detected issue")
    root_cause: str = Field(description="Clear technical explanation of the issue")
    suggested_fixes: List[str] = Field(description="List of practical troubleshooting steps")
    confidence: int = Field(description="Confidence score (0-100) based on log clarity")