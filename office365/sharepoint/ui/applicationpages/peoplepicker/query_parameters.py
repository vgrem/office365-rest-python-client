from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.source import PrincipalSource
from office365.sharepoint.principal.type import PrincipalType
from office365.sharepoint.ui.applicationpages.peoplepicker.query_settings import (
    PeoplePickerQuerySettings,
)


@dataclass
class ClientPeoplePickerQueryParameters(ClientValue):
    """Specifies the properties of a principal query

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

    QueryString: str
    AllowEmailAddresses: bool = True
    AllowMultipleEntities: bool = True
    AllowOnlyEmailAddresses: bool = False
    AllUrlZones: bool = False
    EnabledClaimProviders: Optional[bool] = None
    ForceClaims: bool = False
    MaximumEntitySuggestions: int = 1
    PrincipalSource: PrincipalSource = PrincipalSource.All
    PrincipalType: PrincipalType = PrincipalType.All
    UrlZone: int = 0
    UrlZoneSpecified: bool = False
    SharePointGroupID: int = 0
    QuerySettings: PeoplePickerQuerySettings = field(default_factory=PeoplePickerQuerySettings)
    Required: Optional[bool] = None
    UseSubstrateSearch: Optional[bool] = None
    WebApplicationID: Optional[UUID] = None

    @property
    def entity_type_name(self):
        return "SP.UI.ApplicationPages.ClientPeoplePickerQueryParameters"
