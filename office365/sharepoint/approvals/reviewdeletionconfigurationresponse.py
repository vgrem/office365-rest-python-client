from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class ReviewDeletionConfigurationResponse(ClientValue):
    action: Optional[str] = None
    contract_category_id: Optional[str] = None
    message: Optional[str] = None
