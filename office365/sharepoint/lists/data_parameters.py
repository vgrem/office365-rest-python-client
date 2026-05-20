from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class RenderListFilterDataParameters(ClientValue):
    """Specifies the parameters that are used to retrieve filter data."""

    ExcludeFieldFilteringHtml: Optional[bool] = None
    FieldInternalName: Optional[str] = None
    OverrideScope: Optional[str] = None
    ProcessQStringToCAML: Optional[str] = None
    ViewId: Optional[str] = None
    ViewXml: Optional[str] = None
