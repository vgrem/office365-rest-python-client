from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.localized_text import (
        AccessPackageLocalizedText,
    )


class AccessPackageQuestion(Entity):
    @odata(name="isAnswerEditable")
    @property
    def is_answer_editable(self) -> Optional[bool]:
        """Gets the isAnswerEditable property"""
        return self.properties.get("isAnswerEditable", None)

    @odata(name="isRequired")
    @property
    def is_required(self) -> Optional[bool]:
        """Gets the isRequired property"""
        return self.properties.get("isRequired", None)

    @odata(name="sequence")
    @property
    def sequence(self) -> Optional[int]:
        """Gets the sequence property"""
        return self.properties.get("sequence", None)

    @odata(name="text")
    @property
    def text(self) -> Optional[str]:
        """Gets the text property"""
        return self.properties.get("text", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageQuestion"

    @odata(name="localizations")
    @property
    def localizations(self) -> ClientValueCollection[AccessPackageLocalizedText]:
        """Gets the localizations property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.localized_text import (
            AccessPackageLocalizedText,
        )

        return self.properties.get(
            "localizations", ClientValueCollection[AccessPackageLocalizedText](AccessPackageLocalizedText)
        )
