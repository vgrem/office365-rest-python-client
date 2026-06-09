from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.managed.app.registration import ManagedAppRegistration
from office365.intune.devices.management.managed.ebook.ebook import ManagedEBook
from office365.intune.devices.management.mobileapps.category import MobileAppCategory
from office365.intune.devices.management.mobileapps.mobile_app import MobileApp
from office365.intune.devices.management.mobileapps.relationship import MobileAppRelationship
from office365.intune.devices.management.vpptokens.vpp_token import VppToken
from office365.intune.policies.managed_app import ManagedAppPolicy
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class DeviceAppManagement(Entity):
    """Singleton entity that acts as a container for all device and app management functionality."""

    @odata(name="managedAppRegistrations")
    @property
    def managed_app_registrations(self):
        """"""
        return self.properties.get(
            "managedAppRegistrations",
            EntityCollection(
                self.context, ManagedAppRegistration, ResourcePath("managedAppRegistrations", self.resource_path)
            ),
        )

    @property
    def is_enabled_for_microsoft_store_for_business(self) -> Optional[bool]:
        """Gets the isEnabledForMicrosoftStoreForBusiness property"""
        return self.properties.get("isEnabledForMicrosoftStoreForBusiness", None)

    @property
    def microsoft_store_for_business_language(self) -> Optional[str]:
        """Gets the microsoftStoreForBusinessLanguage property"""
        return self.properties.get("microsoftStoreForBusinessLanguage", None)

    @property
    def microsoft_store_for_business_last_completed_application_sync_time(self) -> datetime:
        """Gets the microsoftStoreForBusinessLastCompletedApplicationSyncTime property"""
        return self.properties.get("microsoftStoreForBusinessLastCompletedApplicationSyncTime", datetime.min)

    @property
    def microsoft_store_for_business_last_successful_sync_date_time(self) -> datetime:
        """Gets the microsoftStoreForBusinessLastSuccessfulSyncDateTime property"""
        return self.properties.get("microsoftStoreForBusinessLastSuccessfulSyncDateTime", datetime.min)

    @property
    def managed_e_books(self) -> EntityCollection[ManagedEBook]:
        """Gets the managedEBooks property"""
        return self.properties.get(
            "managedEBooks",
            EntityCollection[ManagedEBook](
                self.context, ManagedEBook, ResourcePath("managedEBooks", self.resource_path)
            ),
        )

    @property
    def mobile_app_categories(self) -> EntityCollection[MobileAppCategory]:
        """Gets the mobileAppCategories property"""
        return self.properties.get(
            "mobileAppCategories",
            EntityCollection[MobileAppCategory](
                self.context, MobileAppCategory, ResourcePath("mobileAppCategories", self.resource_path)
            ),
        )

    @property
    def mobile_app_relationships(self) -> EntityCollection[MobileAppRelationship]:
        """Gets the mobileAppRelationships property"""
        return self.properties.get(
            "mobileAppRelationships",
            EntityCollection[MobileAppRelationship](
                self.context, MobileAppRelationship, ResourcePath("mobileAppRelationships", self.resource_path)
            ),
        )

    @property
    def mobile_apps(self) -> EntityCollection[MobileApp]:
        """Gets the mobileApps property"""
        return self.properties.get(
            "mobileApps",
            EntityCollection[MobileApp](self.context, MobileApp, ResourcePath("mobileApps", self.resource_path)),
        )

    @property
    def vpp_tokens(self) -> EntityCollection[VppToken]:
        """Gets the vppTokens property"""
        return self.properties.get(
            "vppTokens",
            EntityCollection[VppToken](self.context, VppToken, ResourcePath("vppTokens", self.resource_path)),
        )

    @property
    def managed_app_policies(self) -> EntityCollection[ManagedAppPolicy]:
        """Gets the managedAppPolicies property"""
        return self.properties.get(
            "managedAppPolicies",
            EntityCollection[ManagedAppPolicy](
                self.context, ManagedAppPolicy, ResourcePath("managedAppPolicies", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAppManagement"
