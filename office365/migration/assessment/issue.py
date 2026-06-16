from dataclasses import dataclass


@dataclass
class AssessmentIssue:
    severity: str  # blocker | warning | info
    category: str  # path | field | permission | file | workflow
    location: str  # list/folder/field path
    message: str
    suggestion: str = ""
