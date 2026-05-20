from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SiteScriptActionStatus(ClientValue):
    ActionIndex: Optional[int] = None
    ActionKey: Optional[str] = None
    ActionTitle: Optional[str] = None
    ActionVerb: Optional[str] = None
    LastModified: Optional[int] = None
    OrdinalIndex: Optional[int] = None
    OutcomeCode: Optional[int] = None
    OutcomeText: Optional[str] = None
    SiteScriptID: Optional[str] = None
    SiteScriptIndex: Optional[int] = None
    SiteScriptTitle: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptActionStatus"
