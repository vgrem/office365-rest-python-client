from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ViewCreationInformation(ClientValue):
    """Specifies the properties used to create a new list view."""

    Title: Optional[str] = None
    ViewTypeKind: Optional[int] = None
    ViewFields: StringCollection | None = None
    ViewData: Optional[str] = None
    RowLimit: Optional[int] = None
    Query: Optional[str] = None
    PersonalView: Optional[bool] = None
    Paged: Optional[bool] = None
    AssociatedContentTypeId: Optional[str] = None
    baseViewId: Optional[int] = None
    CalendarViewStyles: Optional[str] = None
    ColumnWidth: Optional[str] = None
    CustomFormatter: Optional[str] = None
    SetAsDefaultView: Optional[bool] = None
    ViewType2: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.ViewCreationInformation"
