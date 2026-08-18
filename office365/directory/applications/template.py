from datetime import date, datetime
from typing import Optional

from office365.directory.applications.application_risk_factors import ApplicationRiskFactors
from office365.directory.applications.application_risk_score import ApplicationRiskScore
from office365.directory.applications.service_principal import ApplicationServicePrincipal
from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection


class ApplicationTemplate(Entity):
    """Represents an application in the Azure AD application gallery."""

    def instantiate(self, display_name: str) -> ApplicationServicePrincipal:
        """Add an instance of an application from the Azure AD application gallery into your directory. You can also use
        this API to instantiate non-gallery apps.
        Use the following ID for the applicationTemplate object: 8adf8e6e-67b2-4cf2-a259-e3dc5476c621.

        Args:
            display_name (str): Custom name of the application
        """
        return_type = ApplicationServicePrincipal(self.context)
        payload = {"displayName": display_name}
        qry = ServiceOperationQuery(self, "instantiate", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def display_name(self) -> Optional[str]:
        """The name of the application."""
        return self.properties.get("displayName", None)

    @property
    def categories(self) -> StringCollection:
        """
        The list of categories for the application. Supported values can be: Collaboration, Business Management,
        Consumer, Content management, CRM, Data services, Developer services, E-commerce, Education, ERP, Finance,
        Health, Human resources, IT infrastructure, Mail, Management, Marketing, Media, Productivity,
        Project management, Telecommunications, Tools, Travel, and Web design & hosting.
        """
        return self.properties.get("categories", StringCollection())

    @property
    def supported_provisioning_types(self) -> StringCollection:
        """The list of provisioning modes supported by this application"""
        return self.properties.get("supportedProvisioningTypes", StringCollection())

    @property
    def supported_single_signon_modes(self) -> StringCollection:
        """
        The list of single sign-on modes supported by this application.
        The supported values are oidc, password, saml, and notSupported.
        """
        return self.properties.get("supportedSingleSignOnModes", StringCollection())

    @property
    def deprecation_date(self) -> Optional[date]:
        """Gets the deprecationDate property"""
        return self.properties.get("deprecationDate", None)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def endpoints(self) -> StringCollection:
        """Gets the endpoints property"""
        return self.properties.get("endpoints", StringCollection(None))

    @property
    def home_page_url(self) -> Optional[str]:
        """Gets the homePageUrl property"""
        return self.properties.get("homePageUrl", None)

    @property
    def is_entra_integrated(self) -> Optional[bool]:
        """Gets the isEntraIntegrated property"""
        return self.properties.get("isEntraIntegrated", None)

    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def logo_url(self) -> Optional[str]:
        """Gets the logoUrl property"""
        return self.properties.get("logoUrl", None)

    @property
    def publisher(self) -> Optional[str]:
        """Gets the publisher property"""
        return self.properties.get("publisher", None)

    @property
    def risk_factors(self) -> ApplicationRiskFactors:
        """Gets the riskFactors property"""
        return self.properties.get("riskFactors", ApplicationRiskFactors())

    @property
    def risk_score(self) -> ApplicationRiskScore:
        """Gets the riskScore property"""
        return self.properties.get("riskScore", ApplicationRiskScore())

    @property
    def supported_single_sign_on_modes(self) -> StringCollection:
        """Gets the supportedSingleSignOnModes property"""
        return self.properties.get("supportedSingleSignOnModes", StringCollection(None))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationTemplate"
