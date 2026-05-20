from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharepointids import SharePointIds
from office365.sharepoint.sites.template import SiteTemplate
from office365.sharepoint.viva.resourcevisualization import ResourceVisualization


@dataclass
class SPAgreementsSite(ClientValue):
    CreatedDateTime: datetime = datetime.min
    Description: Optional[str] = None
    GroupId: Optional[str] = None
    LastModifiedDateTime: datetime = datetime.min
    ResourceVisualization: ResourceVisualization = field(default_factory=ResourceVisualization)
    SharePointIds: SharePointIds = field(default_factory=SharePointIds)
    Template: SiteTemplate = field(default_factory=SiteTemplate)
    Title: Optional[str] = None
    WebUrl: Optional[str] = None
