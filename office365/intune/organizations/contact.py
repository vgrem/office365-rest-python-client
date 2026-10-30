from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.booking.phone import Phone
from office365.directory.objects.collection import DirectoryObjectCollection
from office365.directory.objects.object import DirectoryObject
from office365.directory.objects.onpremisesprovisioningerror import OnPremisesProvisioningError
from office365.directory.objects.serviceprovisioningerror import ServiceProvisioningError
from office365.intune.organizations.physical_office_address import PhysicalOfficeAddress
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.groups.on_premises_sync_behavior import (
        OnPremisesSyncBehavior,
    )


class OrgContact(DirectoryObject):
    """Represents an organizational contact. Organizational contacts are managed by an organization's administrators
    and are different from personal contacts. Additionally, organizational contacts are either synchronized
    from on-premises directories or from Exchange Online, and are read-only."""

    @odata(name="directReports", navigation=True)
    @property
    def direct_reports(self) -> DirectoryObjectCollection:
        """
        Get a user's direct reports.
        """
        return self.properties.get(
            "directReports",
            DirectoryObjectCollection(self.context, ResourcePath("directReports", self.resource_path)),
        )

    @odata(name="manager", navigation=True)
    @property
    def manager(self) -> DirectoryObject:
        """
        The user or contact that is this contact's manager.
        """
        return self.properties.get(
            "manager",
            DirectoryObject(self.context, ResourcePath("manager", self.resource_path)),
        )

    @odata(name="memberOf", navigation=True)
    @property
    def member_of(self) -> DirectoryObjectCollection:
        """Groups that this contact is a member of."""
        return self.properties.get(
            "memberOf",
            DirectoryObjectCollection(self.context, ResourcePath("memberOf", self.resource_path)),
        )

    @odata(name="transitiveMemberOf", navigation=True)
    @property
    def transitive_member_of(self) -> DirectoryObjectCollection:
        """Groups that this contact is a member of, including groups that the contact is nested under."""
        return self.properties.get(
            "transitiveMemberOf",
            DirectoryObjectCollection(self.context, ResourcePath("transitiveMemberOf", self.resource_path)),
        )

    @odata(name="addresses")
    @property
    def addresses(self) -> ClientValueCollection[PhysicalOfficeAddress]:
        """Gets the addresses property"""
        return self.properties.get("addresses", ClientValueCollection[PhysicalOfficeAddress](PhysicalOfficeAddress))

    @odata(name="companyName")
    @property
    def company_name(self) -> Optional[str]:
        """Gets the companyName property"""
        return self.properties.get("companyName", None)

    @odata(name="department")
    @property
    def department(self) -> Optional[str]:
        """Gets the department property"""
        return self.properties.get("department", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="givenName")
    @property
    def given_name(self) -> Optional[str]:
        """Gets the givenName property"""
        return self.properties.get("givenName", None)

    @odata(name="jobTitle")
    @property
    def job_title(self) -> Optional[str]:
        """Gets the jobTitle property"""
        return self.properties.get("jobTitle", None)

    @odata(name="mail")
    @property
    def mail(self) -> Optional[str]:
        """Gets the mail property"""
        return self.properties.get("mail", None)

    @odata(name="mailNickname")
    @property
    def mail_nickname(self) -> Optional[str]:
        """Gets the mailNickname property"""
        return self.properties.get("mailNickname", None)

    @odata(name="onPremisesLastSyncDateTime")
    @property
    def on_premises_last_sync_date_time(self) -> Optional[datetime]:
        """Gets the onPremisesLastSyncDateTime property"""
        return self.properties.get("onPremisesLastSyncDateTime", datetime.min)

    @odata(name="onPremisesProvisioningErrors")
    @property
    def on_premises_provisioning_errors(self) -> ClientValueCollection[OnPremisesProvisioningError]:
        """Gets the onPremisesProvisioningErrors property"""
        return self.properties.get(
            "onPremisesProvisioningErrors",
            ClientValueCollection[OnPremisesProvisioningError](OnPremisesProvisioningError),
        )

    @odata(name="onPremisesSyncEnabled")
    @property
    def on_premises_sync_enabled(self) -> Optional[bool]:
        """Gets the onPremisesSyncEnabled property"""
        return self.properties.get("onPremisesSyncEnabled", None)

    @odata(name="phones")
    @property
    def phones(self) -> ClientValueCollection[Phone]:
        """Gets the phones property"""
        return self.properties.get("phones", ClientValueCollection[Phone](Phone))

    @odata(name="proxyAddresses")
    @property
    def proxy_addresses(self) -> StringCollection:
        """Gets the proxyAddresses property"""
        return self.properties.get("proxyAddresses", StringCollection())

    @odata(name="serviceProvisioningErrors")
    @property
    def service_provisioning_errors(self) -> ClientValueCollection[ServiceProvisioningError]:
        """Gets the serviceProvisioningErrors property"""
        return self.properties.get(
            "serviceProvisioningErrors", ClientValueCollection[ServiceProvisioningError](ServiceProvisioningError)
        )

    @odata(name="surname")
    @property
    def surname(self) -> Optional[str]:
        """Gets the surname property"""
        return self.properties.get("surname", None)

    @odata(name="onPremisesSyncBehavior", navigation=True)
    @property
    def on_premises_sync_behavior(self) -> OnPremisesSyncBehavior:
        """Gets the onPremisesSyncBehavior property"""
        from office365.directory.groups.on_premises_sync_behavior import (
            OnPremisesSyncBehavior,
        )

        return self.properties.get(
            "onPremisesSyncBehavior",
            OnPremisesSyncBehavior(self.context, ResourcePath("onPremisesSyncBehavior", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OrgContact"
