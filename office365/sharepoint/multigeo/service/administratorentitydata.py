from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class GeoAdministratorEntityData(ClientValue):
    DisplayName: Optional[str] = None
    LoginName: Optional[str] = None
    MemberType: Optional[int] = None
    ObjectId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoAdministratorEntityData"
