from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.identities.providers.verified_id_profile_state import VerifiedIdProfileState
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.face_check_configuration import (
        FaceCheckConfiguration,
    )
    from office365.directory.policies.verified_id_profile_configuration import (
        VerifiedIdProfileConfiguration,
    )
    from office365.directory.policies.verified_id_usage_configuration import (
        VerifiedIdUsageConfiguration,
    )


class VerifiedIdProfile(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="faceCheckConfiguration")
    @property
    def face_check_configuration(self) -> FaceCheckConfiguration:
        """Gets the faceCheckConfiguration property"""
        from office365.directory.policies.face_check_configuration import (
            FaceCheckConfiguration,
        )

        return self.properties.get("faceCheckConfiguration", FaceCheckConfiguration())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="priority")
    @property
    def priority(self) -> Optional[int]:
        """Gets the priority property"""
        return self.properties.get("priority", None)

    @odata(name="state")
    @property
    def state(self) -> VerifiedIdProfileState:
        """Gets the state property"""
        return self.properties.get("state", VerifiedIdProfileState.enabled)

    @odata(name="verifiedIdProfileConfiguration")
    @property
    def verified_id_profile_configuration(self) -> VerifiedIdProfileConfiguration:
        """Gets the verifiedIdProfileConfiguration property"""
        from office365.directory.policies.verified_id_profile_configuration import (
            VerifiedIdProfileConfiguration,
        )

        return self.properties.get("verifiedIdProfileConfiguration", VerifiedIdProfileConfiguration())

    @odata(name="verifiedIdUsageConfigurations")
    @property
    def verified_id_usage_configurations(self) -> ClientValueCollection[VerifiedIdUsageConfiguration]:
        """Gets the verifiedIdUsageConfigurations property"""
        from office365.directory.policies.verified_id_usage_configuration import (
            VerifiedIdUsageConfiguration,
        )

        return self.properties.get(
            "verifiedIdUsageConfigurations",
            ClientValueCollection[VerifiedIdUsageConfiguration](VerifiedIdUsageConfiguration),
        )

    @odata(name="verifierDid")
    @property
    def verifier_did(self) -> Optional[str]:
        """Gets the verifierDid property"""
        return self.properties.get("verifierDid", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VerifiedIdProfile"
