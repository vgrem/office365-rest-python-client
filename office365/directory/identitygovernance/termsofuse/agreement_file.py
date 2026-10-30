from __future__ import annotations

from office365.directory.identitygovernance.termsofuse.agreement_file_localization import AgreementFileLocalization
from office365.directory.identitygovernance.termsofuse.agreement_file_properties import (
    AgreementFileProperties,
)
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AgreementFile(AgreementFileProperties):
    @odata(name="localizations", navigation=True)
    @property
    def localizations(self) -> EntityCollection[AgreementFileLocalization]:
        """Gets the localizations property"""
        return self.properties.get(
            "localizations",
            EntityCollection[AgreementFileLocalization](
                self.context, AgreementFileLocalization, ResourcePath("localizations", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AgreementFile"
