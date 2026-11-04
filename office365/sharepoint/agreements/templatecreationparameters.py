from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TemplateCreationParameters(ClientValue):
    SourceFileUniqueId: Optional[str] = None
    SourceLibraryId: Optional[str] = None
    TemplateName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.TemplateCreationParameters"
