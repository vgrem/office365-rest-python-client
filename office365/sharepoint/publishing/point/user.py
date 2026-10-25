from __future__ import annotations

from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class PointPublishingUser(Entity):
    @odata(name="AccountName")
    @property
    def account_name(self) -> Optional[str]:
        """Gets the AccountName property"""
        return self.properties.get("AccountName", None)

    @odata(name="Department")
    @property
    def department(self) -> Optional[str]:
        """Gets the Department property"""
        return self.properties.get("Department", None)

    @odata(name="Email")
    @property
    def email(self) -> Optional[str]:
        """Gets the Email property"""
        return self.properties.get("Email", None)

    @odata(name="ID")
    @property
    def id_(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @odata(name="IsDomainGroup")
    @property
    def is_domain_group(self) -> Optional[bool]:
        """Gets the IsDomainGroup property"""
        return self.properties.get("IsDomainGroup", None)

    @odata(name="IsMagazineOwner")
    @property
    def is_magazine_owner(self) -> Optional[bool]:
        """Gets the IsMagazineOwner property"""
        return self.properties.get("IsMagazineOwner", None)

    @odata(name="JobTitle")
    @property
    def job_title(self) -> Optional[str]:
        """Gets the JobTitle property"""
        return self.properties.get("JobTitle", None)

    @odata(name="LoginName")
    @property
    def login_name(self) -> Optional[str]:
        """Gets the LoginName property"""
        return self.properties.get("LoginName", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="PictureUrl")
    @property
    def picture_url(self) -> Optional[str]:
        """Gets the PictureUrl property"""
        return self.properties.get("PictureUrl", None)

    @odata(name="SipAddress")
    @property
    def sip_address(self) -> Optional[str]:
        """Gets the SipAddress property"""
        return self.properties.get("SipAddress", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PointPublishingUser"

    def delete_user_from_container_group(self) -> Self:
        """DeleteUserFromContainerGroup operation."""
        qry = ServiceOperationQuery(self, "DeleteUserFromContainerGroup", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="ID")
    @property
    def id(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)
