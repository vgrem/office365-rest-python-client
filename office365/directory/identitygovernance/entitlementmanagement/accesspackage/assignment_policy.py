from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment_approval_settings import (  # noqa: E501
    AccessPackageAssignmentApprovalSettings,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment_requestor_settings import (  # noqa: E501
    AccessPackageAssignmentRequestorSettings,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment_review_settings import (  # noqa: E501
    AccessPackageAssignmentReviewSettings,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.automatic_request_settings import (  # noqa: E501
    AccessPackageAutomaticRequestSettings,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.expiration_pattern import (  # noqa: E501
    ExpirationPattern,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.notification_settings import (  # noqa: E501
    AccessPackageNotificationSettings,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.question import (
    AccessPackageQuestion,
)
from office365.directory.identitygovernance.workflow.custom_extension_stage_setting import (
    CustomExtensionStageSetting,
)
from office365.directory.policies.allowedtargetscope import AllowedTargetScope
from office365.directory.subjectset import SubjectSet
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.catalog import (
        AccessPackageCatalog,
    )
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.package import (
        AccessPackage,
    )


class AccessPackageAssignmentPolicy(Entity):
    @odata(name="allowedTargetScope")
    @property
    def allowed_target_scope(self) -> AllowedTargetScope:
        """Gets the allowedTargetScope property"""
        return self.properties.get("allowedTargetScope", AllowedTargetScope.notSpecified)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="modifiedDateTime")
    @property
    def modified_date_time(self) -> datetime:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @odata(name="specificAllowedTargets")
    @property
    def specific_allowed_targets(self) -> ClientValueCollection[SubjectSet]:
        """Gets the specificAllowedTargets property"""
        return self.properties.get("specificAllowedTargets", ClientValueCollection[SubjectSet](SubjectSet))

    @odata(name="customExtensionStageSettings", navigation=True)
    @property
    def custom_extension_stage_settings(self) -> EntityCollection[CustomExtensionStageSetting]:
        """Gets the customExtensionStageSettings property"""
        return self.properties.get(
            "customExtensionStageSettings",
            EntityCollection[CustomExtensionStageSetting](
                self.context,
                CustomExtensionStageSetting,
                ResourcePath("customExtensionStageSettings", self.resource_path),
            ),
        )

    @odata(name="questions", navigation=True)
    @property
    def questions(self) -> EntityCollection[AccessPackageQuestion]:
        """Gets the questions property"""
        return self.properties.get(
            "questions",
            EntityCollection[AccessPackageQuestion](
                self.context, AccessPackageQuestion, ResourcePath("questions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentPolicy"

    @odata(name="automaticRequestSettings")
    @property
    def automatic_request_settings(self) -> AccessPackageAutomaticRequestSettings:
        """Gets the automaticRequestSettings property"""
        return self.properties.get("automaticRequestSettings", AccessPackageAutomaticRequestSettings())

    @odata(name="expiration")
    @property
    def expiration(self) -> ExpirationPattern:
        """Gets the expiration property"""
        return self.properties.get("expiration", ExpirationPattern())

    @odata(name="notificationSettings")
    @property
    def notification_settings(self) -> AccessPackageNotificationSettings:
        """Gets the notificationSettings property"""
        return self.properties.get("notificationSettings", AccessPackageNotificationSettings())

    @odata(name="requestApprovalSettings")
    @property
    def request_approval_settings(self) -> AccessPackageAssignmentApprovalSettings:
        """Gets the requestApprovalSettings property"""
        return self.properties.get("requestApprovalSettings", AccessPackageAssignmentApprovalSettings())

    @odata(name="requestorSettings")
    @property
    def requestor_settings(self) -> AccessPackageAssignmentRequestorSettings:
        """Gets the requestorSettings property"""
        return self.properties.get("requestorSettings", AccessPackageAssignmentRequestorSettings())

    @odata(name="reviewSettings")
    @property
    def review_settings(self) -> AccessPackageAssignmentReviewSettings:
        """Gets the reviewSettings property"""
        return self.properties.get("reviewSettings", AccessPackageAssignmentReviewSettings())

    @odata(name="accessPackage", navigation=True)
    @property
    def access_package(self) -> AccessPackage:
        """Gets the accessPackage property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.package import (
            AccessPackage,
        )

        return self.properties.get(
            "accessPackage", AccessPackage(self.context, ResourcePath("accessPackage", self.resource_path))
        )

    @odata(name="catalog", navigation=True)
    @property
    def catalog(self) -> AccessPackageCatalog:
        """Gets the catalog property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.catalog import (
            AccessPackageCatalog,
        )

        return self.properties.get(
            "catalog", AccessPackageCatalog(self.context, ResourcePath("catalog", self.resource_path))
        )
