from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.authoringschemafeatureversion import (
    AuthoringSchemaFeatureVersion,
)


class StartCoAuthMetaData(ClientValue):

    def __init__(
        self,
        authoring_schema_feature_versions: ClientValueCollection[AuthoringSchemaFeatureVersion] = ClientValueCollection(
            AuthoringSchemaFeatureVersion
        ),
        force_checkin: bool = None,
        force_flush_op_stream: bool = None,
        is_user_consent_provided_for_moderation_status: bool = None,
    ):
        self.AuthoringSchemaFeatureVersions = authoring_schema_feature_versions
        self.ForceCheckin = force_checkin
        self.ForceFlushOpStream = force_flush_op_stream
        self.IsUserConsentProvidedForModerationStatus = is_user_consent_provided_for_moderation_status

    @property
    def entity_type_name(self):
        return "SP.Publishing.StartCoAuthMetaData"
