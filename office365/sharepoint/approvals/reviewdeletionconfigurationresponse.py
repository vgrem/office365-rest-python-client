from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ReviewDeletionConfigurationResponse(ClientValue):
    action: Optional[str] = None
    contract_category_id: Optional[str] = None
    message: Optional[str] = None
