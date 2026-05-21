from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteCreationData(ClientValue):
    Count = None
    SiteCreationSourceGuid = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCreationData"
