from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.validations.errorcodesforemail import (
    PrePublishValidationsErrorCodesForEmail,
)
from office365.sharepoint.publishing.validations.errorcodesforsharepointsite import (
    PrePublishValidationsErrorCodesForSharePointSite,
)
from office365.sharepoint.publishing.validations.errorcodesforteams import (
    PrePublishValidationsErrorCodesForTeams as _PrePublishValidationsErrorCodesForTeams,
)
from office365.sharepoint.publishing.validations.prepublishvalidationserrorcodesforvivaengage import (
    PrePublishValidationsErrorCodesForVivaEngage as _PrePublishValidationsErrorCodesForVivaEngage,
)


@dataclass
class PrePublishValidationsResponse(ClientValue):
    ErrorCodes: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))
    PrePublishValidationsErrorCodesForEmails: ClientValueCollection[PrePublishValidationsErrorCodesForEmail] = field(
        default_factory=lambda: ClientValueCollection(PrePublishValidationsErrorCodesForEmail)
    )
    PrePublishValidationsErrorCodesForSharePointSites: ClientValueCollection[
        PrePublishValidationsErrorCodesForSharePointSite
    ] = field(default_factory=lambda: ClientValueCollection(PrePublishValidationsErrorCodesForSharePointSite))
    PrePublishValidationsErrorCodesForTeams: Optional[
        ClientValueCollection[_PrePublishValidationsErrorCodesForTeams]
    ] = None
    PrePublishValidationsErrorCodesForVivaEngage: Optional[_PrePublishValidationsErrorCodesForVivaEngage] = None
    PrePublishValidationsErrorCodesForVivaEngageV2: ClientValueCollection[
        _PrePublishValidationsErrorCodesForVivaEngage
    ] = field(default_factory=lambda: ClientValueCollection(_PrePublishValidationsErrorCodesForVivaEngage))

    @property
    def entity_type_name(self):
        return "SP.Publishing.PrePublishValidationsResponse"
