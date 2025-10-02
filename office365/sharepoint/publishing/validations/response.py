from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.validations.errorcodesforemail import (
    PrePublishValidationsErrorCodesForEmail,
)
from office365.sharepoint.publishing.validations.errorcodesforsharepointsite import (
    PrePublishValidationsErrorCodesForSharePointSite,
)
from office365.sharepoint.publishing.validations.errorcodesforteams import (
    PrePublishValidationsErrorCodesForTeams,
)
from office365.sharepoint.publishing.validations.prepublishvalidationserrorcodesforvivaengage import (
    PrePublishValidationsErrorCodesForVivaEngage,
)


class PrePublishValidationsResponse(ClientValue):

    def __init__(
        self,
        error_codes: ClientValueCollection[int] = ClientValueCollection(int),
        pre_publish_validations_error_codes_for_emails: ClientValueCollection[
            PrePublishValidationsErrorCodesForEmail
        ] = ClientValueCollection(PrePublishValidationsErrorCodesForEmail),
        pre_publish_validations_error_codes_for_share_point_sites: ClientValueCollection[
            PrePublishValidationsErrorCodesForSharePointSite
        ] = ClientValueCollection(
            PrePublishValidationsErrorCodesForSharePointSite
        ),
        pre_publish_validations_error_codes_for_teams: ClientValueCollection[
            PrePublishValidationsErrorCodesForTeams
        ] = None,
        pre_publish_validations_error_codes_for_viva_engage: PrePublishValidationsErrorCodesForVivaEngage = None,
        pre_publish_validations_error_codes_for_viva_engage_v2: ClientValueCollection[
            PrePublishValidationsErrorCodesForVivaEngage
        ] = ClientValueCollection(PrePublishValidationsErrorCodesForVivaEngage),
    ):
        self.ErrorCodes = error_codes
        self.PrePublishValidationsErrorCodesForEmails = (
            pre_publish_validations_error_codes_for_emails
        )
        self.PrePublishValidationsErrorCodesForSharePointSites = (
            pre_publish_validations_error_codes_for_share_point_sites
        )
        self.PrePublishValidationsErrorCodesForTeams = (
            pre_publish_validations_error_codes_for_teams
        )
        self.PrePublishValidationsErrorCodesForVivaEngage = (
            pre_publish_validations_error_codes_for_viva_engage
        )
        self.PrePublishValidationsErrorCodesForVivaEngageV2 = (
            pre_publish_validations_error_codes_for_viva_engage_v2
        )
