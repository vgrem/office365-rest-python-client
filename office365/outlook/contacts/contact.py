from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.directory.extensions.extended_property import (
    MultiValueLegacyExtendedProperty,
    SingleValueLegacyExtendedProperty,
)
from office365.directory.extensions.extension import Extension
from office365.directory.permissions.require_permission import require_permission
from office365.directory.profile_photo import ProfilePhoto
from office365.entity_collection import EntityCollection
from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.item import OutlookItem
from office365.outlook.mail.physical_address import PhysicalAddress
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class Contact(OutlookItem):
    """User's contact."""

    @require_permission(
        delegated=["Contacts.ReadWrite"], application=["Contacts.ReadWrite"], notes="Permanently delete a contact"
    )
    def permanent_delete(self) -> Self:
        """Permanently delete a contact and place it in the purges folder in the dumpster in the user's mailbox.
        Email clients such as outlook or outlook on the web can't access permanently deleted items. Unless there's
        a hold set on the mailbox, the items are permanently deleted after a set period of time.
        """
        qry = ServiceOperationQuery(self, "permanentDelete")
        self.context.add_query(qry)
        return self

    @odata(name="businessPhones")
    @property
    def business_phones(self) -> StringCollection:
        """The contact's business phone numbers."""
        return self.properties.setdefault("businessPhones", StringCollection())

    @property
    def display_name(self) -> Optional[str]:
        """
        The contact's display name. You can specify the display name in a create or update operation.
        Note that later updates to other properties may cause an automatically generated value to overwrite the
        displayName value you have specified. To preserve a pre-existing value, always include it as displayName
        in an update operation.
        """
        return self.properties.get("displayName", None)

    @property
    def manager(self) -> Optional[str]:
        """
        The name of the contact's manager.
        """
        return self.properties.get("manager", None)

    @manager.setter
    def manager(self, value: str) -> None:
        """Sets name of the contact's manager."""
        self.set_property("manager", value)

    @property
    def mobile_phone(self) -> Optional[str]:
        """The contact's mobile phone number."""
        return self.properties.get("mobilePhone", None)

    @mobile_phone.setter
    def mobile_phone(self, value: str) -> None:
        """Sets contact's mobile phone number."""
        self.set_property("mobilePhone", value)

    @odata(name="homeAddress")
    @property
    def home_address(self) -> PhysicalAddress:
        """The contact's home address."""
        return self.properties.get("homeAddress", PhysicalAddress())

    @odata(name="emailAddresses")
    @property
    def email_addresses(self) -> ClientValueCollection[EmailAddress]:
        """The contact's email addresses."""
        return self.properties.setdefault("emailAddresses", ClientValueCollection(EmailAddress))

    @property
    def extensions(self) -> EntityCollection[Extension]:
        """The collection of open extensions defined for the contact. Nullable."""
        return self.properties.get(
            "extensions", EntityCollection(self.context, Extension, ResourcePath("extensions", self.resource_path))
        )

    @property
    def photo(self) -> ProfilePhoto:
        """Optional contact picture. You can get or set a photo for a contact."""
        return self.properties.get("photo", ProfilePhoto(self.context, ResourcePath("photo", self.resource_path)))

    @odata(name="multiValueExtendedProperties")
    @property
    def multi_value_extended_properties(self) -> EntityCollection[MultiValueLegacyExtendedProperty]:
        """The collection of multi-value extended properties defined for the Contact."""
        return self.properties.get(
            "multiValueExtendedProperties",
            EntityCollection(
                self.context,
                MultiValueLegacyExtendedProperty,
                ResourcePath("multiValueExtendedProperties", self.resource_path),
            ),
        )

    @odata(name="singleValueExtendedProperties")
    @property
    def single_value_extended_properties(self) -> EntityCollection[SingleValueLegacyExtendedProperty]:
        """The collection of single-value extended properties defined for the Contact."""
        return self.properties.get(
            "singleValueExtendedProperties",
            EntityCollection(
                self.context,
                SingleValueLegacyExtendedProperty,
                ResourcePath("singleValueExtendedProperties", self.resource_path),
            ),
        )

    @property
    def assistant_name(self) -> Optional[str]:
        """Gets the assistantName property"""
        return self.properties.get("assistantName", None)

    @property
    def birthday(self) -> datetime:
        """Gets the birthday property"""
        return self.properties.get("birthday", datetime.min)

    @property
    def business_address(self) -> PhysicalAddress:
        """Gets the businessAddress property"""
        return self.properties.get("businessAddress", PhysicalAddress())

    @property
    def business_home_page(self) -> Optional[str]:
        """Gets the businessHomePage property"""
        return self.properties.get("businessHomePage", None)

    @property
    def children(self) -> StringCollection:
        """Gets the children property"""
        return self.properties.get("children", StringCollection(None))

    @property
    def company_name(self) -> Optional[str]:
        """Gets the companyName property"""
        return self.properties.get("companyName", None)

    @property
    def department(self) -> Optional[str]:
        """Gets the department property"""
        return self.properties.get("department", None)

    @property
    def file_as(self) -> Optional[str]:
        """Gets the fileAs property"""
        return self.properties.get("fileAs", None)

    @property
    def generation(self) -> Optional[str]:
        """Gets the generation property"""
        return self.properties.get("generation", None)

    @property
    def given_name(self) -> Optional[str]:
        """Gets the givenName property"""
        return self.properties.get("givenName", None)

    @property
    def home_phones(self) -> StringCollection:
        """Gets the homePhones property"""
        return self.properties.get("homePhones", StringCollection(None))

    @property
    def im_addresses(self) -> StringCollection:
        """Gets the imAddresses property"""
        return self.properties.get("imAddresses", StringCollection(None))

    @property
    def initials(self) -> Optional[str]:
        """Gets the initials property"""
        return self.properties.get("initials", None)

    @property
    def job_title(self) -> Optional[str]:
        """Gets the jobTitle property"""
        return self.properties.get("jobTitle", None)

    @property
    def middle_name(self) -> Optional[str]:
        """Gets the middleName property"""
        return self.properties.get("middleName", None)

    @property
    def nick_name(self) -> Optional[str]:
        """Gets the nickName property"""
        return self.properties.get("nickName", None)

    @property
    def office_location(self) -> Optional[str]:
        """Gets the officeLocation property"""
        return self.properties.get("officeLocation", None)

    @property
    def other_address(self) -> PhysicalAddress:
        """Gets the otherAddress property"""
        return self.properties.get("otherAddress", PhysicalAddress())

    @property
    def parent_folder_id(self) -> Optional[str]:
        """Gets the parentFolderId property"""
        return self.properties.get("parentFolderId", None)

    @property
    def personal_notes(self) -> Optional[str]:
        """Gets the personalNotes property"""
        return self.properties.get("personalNotes", None)

    @property
    def primary_email_address(self) -> EmailAddress:
        """Gets the primaryEmailAddress property"""
        return self.properties.get("primaryEmailAddress", EmailAddress())

    @property
    def profession(self) -> Optional[str]:
        """Gets the profession property"""
        return self.properties.get("profession", None)

    @property
    def secondary_email_address(self) -> EmailAddress:
        """Gets the secondaryEmailAddress property"""
        return self.properties.get("secondaryEmailAddress", EmailAddress())

    @property
    def spouse_name(self) -> Optional[str]:
        """Gets the spouseName property"""
        return self.properties.get("spouseName", None)

    @property
    def surname(self) -> Optional[str]:
        """Gets the surname property"""
        return self.properties.get("surname", None)

    @property
    def tertiary_email_address(self) -> EmailAddress:
        """Gets the tertiaryEmailAddress property"""
        return self.properties.get("tertiaryEmailAddress", EmailAddress())

    @property
    def title(self) -> Optional[str]:
        """Gets the title property"""
        return self.properties.get("title", None)

    @property
    def yomi_company_name(self) -> Optional[str]:
        """Gets the yomiCompanyName property"""
        return self.properties.get("yomiCompanyName", None)

    @property
    def yomi_given_name(self) -> Optional[str]:
        """Gets the yomiGivenName property"""
        return self.properties.get("yomiGivenName", None)

    @property
    def yomi_surname(self) -> Optional[str]:
        """Gets the yomiSurname property"""
        return self.properties.get("yomiSurname", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Contact"
