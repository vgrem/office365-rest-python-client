from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection


class AnalyzedEmail(Entity):
    @property
    def alert_ids(self) -> StringCollection:
        """Gets the alertIds property"""
        return self.properties.get("alertIds", StringCollection(None))

    @property
    def bulk_complaint_level(self) -> Optional[str]:
        """Gets the bulkComplaintLevel property"""
        return self.properties.get("bulkComplaintLevel", None)

    @property
    def client_type(self) -> Optional[str]:
        """Gets the clientType property"""
        return self.properties.get("clientType", None)

    @property
    def contexts(self) -> StringCollection:
        """Gets the contexts property"""
        return self.properties.get("contexts", StringCollection(None))

    @property
    def detection_methods(self) -> StringCollection:
        """Gets the detectionMethods property"""
        return self.properties.get("detectionMethods", StringCollection(None))

    @property
    def distribution_list(self) -> Optional[str]:
        """Gets the distributionList property"""
        return self.properties.get("distributionList", None)

    @property
    def email_cluster_id(self) -> Optional[str]:
        """Gets the emailClusterId property"""
        return self.properties.get("emailClusterId", None)

    @property
    def forwarding_detail(self) -> Optional[str]:
        """Gets the forwardingDetail property"""
        return self.properties.get("forwardingDetail", None)

    @property
    def inbound_connector_formatted_name(self) -> Optional[str]:
        """Gets the inboundConnectorFormattedName property"""
        return self.properties.get("inboundConnectorFormattedName", None)

    @property
    def internet_message_id(self) -> Optional[str]:
        """Gets the internetMessageId property"""
        return self.properties.get("internetMessageId", None)

    @property
    def language(self) -> Optional[str]:
        """Gets the language property"""
        return self.properties.get("language", None)

    @property
    def logged_date_time(self) -> Optional[datetime]:
        """Gets the loggedDateTime property"""
        return self.properties.get("loggedDateTime", datetime.min)

    @property
    def network_message_id(self) -> Optional[str]:
        """Gets the networkMessageId property"""
        return self.properties.get("networkMessageId", None)

    @property
    def override_sources(self) -> StringCollection:
        """Gets the overrideSources property"""
        return self.properties.get("overrideSources", StringCollection(None))

    @property
    def phish_confidence_level(self) -> Optional[str]:
        """Gets the phishConfidenceLevel property"""
        return self.properties.get("phishConfidenceLevel", None)

    @property
    def policy(self) -> Optional[str]:
        """Gets the policy property"""
        return self.properties.get("policy", None)

    @property
    def policy_action(self) -> Optional[str]:
        """Gets the policyAction property"""
        return self.properties.get("policyAction", None)

    @property
    def policy_type(self) -> Optional[str]:
        """Gets the policyType property"""
        return self.properties.get("policyType", None)

    @property
    def primary_override_source(self) -> Optional[str]:
        """Gets the primaryOverrideSource property"""
        return self.properties.get("primaryOverrideSource", None)

    @property
    def recipient_email_address(self) -> Optional[str]:
        """Gets the recipientEmailAddress property"""
        return self.properties.get("recipientEmailAddress", None)

    @property
    def return_path(self) -> Optional[str]:
        """Gets the returnPath property"""
        return self.properties.get("returnPath", None)

    @property
    def size_in_bytes(self) -> Optional[int]:
        """Gets the sizeInBytes property"""
        return self.properties.get("sizeInBytes", None)

    @property
    def spam_confidence_level(self) -> Optional[str]:
        """Gets the spamConfidenceLevel property"""
        return self.properties.get("spamConfidenceLevel", None)

    @property
    def subject(self) -> Optional[str]:
        """Gets the subject property"""
        return self.properties.get("subject", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AnalyzedEmail"
