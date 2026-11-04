from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SMARetirePageMinimumAgeFeedbackSignal(ClientValue):
    DefaultAge: Optional[int] = None
    FromDismissAction: Optional[int] = None
    FromEmptyState: Optional[int] = None
    PreferredAge: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SMARetirePageMinimumAgeFeedbackSignal"
