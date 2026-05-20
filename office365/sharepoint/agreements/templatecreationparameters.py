from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TemplateCreationParameters(ClientValue):
    SourceFileUniqueId: Optional[str] = None
    SourceLibraryId: Optional[str] = None
    TemplateName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.TemplateCreationParameters"
