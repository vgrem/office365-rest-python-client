from office365.entity import Entity
from dataclasses import dataclass, field
from office365.runtime.paths.resource_path import ResourcePath

class ApplicationServicePrincipal(Entity):
    application: Application | None = None
    servicePrincipal: ServicePrincipal | None = None
    '\n    When an instance of an application from the Azure AD application gallery is added, application and servicePrincipal\n     objects are created in the directory. The applicationServicePrincipal represents the concatenation of the\n     application and servicePrincipal object.\n    '

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.ApplicationServicePrincipal'