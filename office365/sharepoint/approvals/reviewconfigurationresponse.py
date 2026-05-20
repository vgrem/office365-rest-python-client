from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.approvals.user import UserDTO


@dataclass
class ReviewConfigurationResponse(ClientValue):
    action: Optional[str] = None
    contract_category: Optional[str] = None
    contract_category_id: Optional[str] = None
    reviewers: ClientValueCollection[UserDTO] = field(default_factory=lambda: ClientValueCollection(UserDTO))
    review_type: Optional[str] = None
