from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.identitygovernance.accessreview.custom_data_provided_resource_upload_stats import (  # noqa: E501
    CustomDataProvidedResourceUploadStats,
)
from office365.directory.identitygovernance.data import Data
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.custom_data_provided_resource_upload_status import (  # noqa: E501
    CustomDataProvidedResourceUploadStatus,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.custom_data_provided_resource_file import (  # noqa: E501
        CustomDataProvidedResourceFile,
    )


class CustomDataProvidedResourceUploadSession(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="data")
    @property
    def data(self) -> Data:
        """Gets the data property"""
        return self.properties.get("data", Data())

    @odata(name="isUploadDone")
    @property
    def is_upload_done(self) -> Optional[bool]:
        """Gets the isUploadDone property"""
        return self.properties.get("isUploadDone", None)

    @odata(name="referenceId")
    @property
    def reference_id(self) -> Optional[str]:
        """Gets the referenceId property"""
        return self.properties.get("referenceId", None)

    @odata(name="stats")
    @property
    def stats(self) -> CustomDataProvidedResourceUploadStats:
        """Gets the stats property"""
        return self.properties.get("stats", CustomDataProvidedResourceUploadStats())

    @odata(name="status")
    @property
    def status(self) -> CustomDataProvidedResourceUploadStatus:
        """Gets the status property"""
        return self.properties.get("status", CustomDataProvidedResourceUploadStatus.active)

    @odata(name="files", navigation=True)
    @property
    def files(self) -> EntityCollection[CustomDataProvidedResourceFile]:
        """Gets the files property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.custom_data_provided_resource_file import (  # noqa: E501
            CustomDataProvidedResourceFile,
        )

        return self.properties.get(
            "files",
            EntityCollection[CustomDataProvidedResourceFile](
                self.context, CustomDataProvidedResourceFile, ResourcePath("files", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomDataProvidedResourceUploadSession"
