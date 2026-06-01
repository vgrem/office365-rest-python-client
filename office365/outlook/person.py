from typing import Optional

from office365.booking.phone import Phone
from office365.entity import Entity
from office365.outlook.mail.location import Location
from office365.runtime.client_value_collection import ClientValueCollection


class Person(Entity):
    """Represents an aggregation of information about a person from across mail and contacts.
    People can be local contacts or your organization's directory, and people from recent communications
    (such as email)."""

    @property
    def birthday(self) -> Optional[str]:
        """Gets the birthday property"""
        return self.properties.get("birthday", None)

    @property
    def company_name(self) -> Optional[str]:
        """Gets the companyName property"""
        return self.properties.get("companyName", None)

    @property
    def department(self) -> Optional[str]:
        """Gets the department property"""
        return self.properties.get("department", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def given_name(self) -> Optional[str]:
        """Gets the givenName property"""
        return self.properties.get("givenName", None)

    @property
    def im_address(self) -> Optional[str]:
        """Gets the imAddress property"""
        return self.properties.get("imAddress", None)

    @property
    def is_favorite(self) -> Optional[bool]:
        """Gets the isFavorite property"""
        return self.properties.get("isFavorite", None)

    @property
    def job_title(self) -> Optional[str]:
        """Gets the jobTitle property"""
        return self.properties.get("jobTitle", None)

    @property
    def office_location(self) -> Optional[str]:
        """Gets the officeLocation property"""
        return self.properties.get("officeLocation", None)

    @property
    def person_notes(self) -> Optional[str]:
        """Gets the personNotes property"""
        return self.properties.get("personNotes", None)

    @property
    def phones(self) -> ClientValueCollection[Phone]:
        """Gets the phones property"""
        return self.properties.get("phones", ClientValueCollection[Phone](Phone))

    @property
    def postal_addresses(self) -> ClientValueCollection[Location]:
        """Gets the postalAddresses property"""
        return self.properties.get("postalAddresses", ClientValueCollection[Location](Location))

    @property
    def profession(self) -> Optional[str]:
        """Gets the profession property"""
        return self.properties.get("profession", None)

    @property
    def surname(self) -> Optional[str]:
        """Gets the surname property"""
        return self.properties.get("surname", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def yomi_company(self) -> Optional[str]:
        """Gets the yomiCompany property"""
        return self.properties.get("yomiCompany", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Person"
