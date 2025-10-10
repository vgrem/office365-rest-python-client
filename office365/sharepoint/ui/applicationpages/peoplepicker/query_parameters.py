from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.source import PrincipalSource
from office365.sharepoint.principal.type import PrincipalType
from office365.sharepoint.ui.applicationpages.peoplepicker.query_settings import (
    PeoplePickerQuerySettings,
)


class ClientPeoplePickerQueryParameters(ClientValue):

    def __init__(
        self,
        query_string: str,
        allow_emai_addresses: bool = True,
        allow_multiple_entities=True,
        allow_only_email_addresses=False,
        all_url_zones=False,
        enabled_claim_providers=None,
        force_claims=False,
        maximum_entity_suggestions=1,
        principal_source: PrincipalSource = PrincipalSource.All,
        principal_type: PrincipalType = PrincipalType.All,
        url_zone: int = 0,
        url_zone_specified: bool = False,
        sharepoint_group_id: int = 0,
        allow_email_addresses: bool = None,
        query_settings: PeoplePickerQuerySettings = PeoplePickerQuerySettings(),
        required: bool = None,
        share_point_group_id: int = None,
        use_substrate_search: bool = None,
        web_application_id: UUID = None,
    ):
        """
        Specifies the properties of a principal query

        :type int urlZone: Specifies a location in the topology of the farm for the principal query.
        :param int sharepoint_group_id: specifies a group containing allowed principals to be used in the principal query
        :param str query_string: Specifies the value to be used in the principal query.
        :param int principal_type: Specifies the type to be used in the principal query.
        :param int principal_source: Specifies the source to be used in the principal query.
        :param int maximum_entity_suggestions: Specifies the maximum number of principals to be returned by the
        principal query.
        :param bool force_claims: Specifies whether the principal query SHOULD be handled by claims providers.
        :param bool enabled_claim_providers: Specifies the claims providers to be used in the principal query.
        :param bool all_url_zones: Specifies whether the principal query will search all locations in the topology
        of the farm.
        :param bool allow_only_email_addresses: Specifies whether to allow the picker to resolve only email addresses as
        valid entities. This property is only used when AllowEmailAddresses (section 3.2.5.217.1.1.1) is set to True.
        Otherwise it is ignored.
        :param bool allow_multiple_entities: Specifies whether the principal query allows multiple values.
        :param bool allow_emai_addresses: Specifies whether the principal query can return a resolved principal
        matching an unverified e-mail address when unable to resolve to a known principal.
        """
        super(ClientPeoplePickerQueryParameters, self).__init__()
        self.QueryString = query_string
        self.AllowEmailAddresses = allow_emai_addresses
        self.AllowMultipleEntities = allow_multiple_entities
        self.AllowOnlyEmailAddresses = allow_only_email_addresses
        self.AllUrlZones = all_url_zones
        self.EnabledClaimProviders = enabled_claim_providers
        self.ForceClaims = force_claims
        self.MaximumEntitySuggestions = maximum_entity_suggestions
        self.PrincipalSource = principal_source
        self.PrincipalType = principal_type
        self.UrlZone = url_zone
        self.UrlZoneSpecified = url_zone_specified
        self.SharePointGroupID = sharepoint_group_id
        self.AllowEmailAddresses = allow_email_addresses
        self.QuerySettings = query_settings
        self.Required = required
        self.SharePointGroupID = share_point_group_id
        self.UseSubstrateSearch = use_substrate_search
        self.WebApplicationID = web_application_id

    @property
    def entity_type_name(self):
        return "SP.UI.ApplicationPages.ClientPeoplePickerQueryParameters"
