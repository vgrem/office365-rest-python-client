from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class ReviewConfigurationPayload(ClientValue):
    category_id: Optional[str] = None
    reviewers: StringCollection = field(default_factory=StringCollection)
    review_type: Optional[str] = None
