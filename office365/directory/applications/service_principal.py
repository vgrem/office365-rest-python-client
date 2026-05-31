from __future__ import annotations

from office365.directory.applications.application import Application
from office365.directory.serviceprincipals.service_principal import ServicePrincipal
from office365.entity import Entity


class ApplicationServicePrincipal(Entity):
    application: Application | None = None
    servicePrincipal: ServicePrincipal | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationServicePrincipal"
