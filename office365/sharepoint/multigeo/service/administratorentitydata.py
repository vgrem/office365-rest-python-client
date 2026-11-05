from typing import Optional

from office365.runtime.client_value import ClientValue


class GeoAdministratorEntityData(ClientValue):
    DisplayName: Optional[str] = None
    LoginName: Optional[str] = None
    MemberType: Optional[int] = None
    ObjectId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoAdministratorEntityData"
