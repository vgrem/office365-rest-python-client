from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SiteScriptActionResult(ClientValue):
    """Represents the result of a site script action execution.

    Args:
        outcome_text (str):
        target (str):
    """

    OutcomeText: Optional[str] = None
    Target: Optional[str] = None
    ErrorCode: Optional[int] = None
    Outcome: Optional[int] = None
    TargetId: Optional[str] = None
    Title: Optional[str] = None
    Verb: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptActionResult"
