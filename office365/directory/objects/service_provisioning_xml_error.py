from __future__ import annotations

from office365.directory.objects.serviceprovisioningerror import ServiceProvisioningError


class ServiceProvisioningXmlError(ServiceProvisioningError):
    errorDetail: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ServiceProvisioningXmlError"
