from __future__ import annotations

from typing import Optional

from office365.directory.authentication.signing_certificate_update_status import SigningCertificateUpdateStatus
from office365.directory.domains.federatedidpmfabehavior import FederatedIdpMfaBehavior
from office365.directory.domains.promptloginbehavior import PromptLoginBehavior
from office365.entity import Entity
from office365.intune.devices.management.system_browser_enabled_on import SystemBrowserEnabledOn
from office365.runtime.types.odata_property import odata


class InternalDomainFederation(Entity):
    @odata(name="activeSignInUri")
    @property
    def active_sign_in_uri(self) -> Optional[str]:
        """Gets the activeSignInUri property"""
        return self.properties.get("activeSignInUri", None)

    @odata(name="federatedIdpMfaBehavior")
    @property
    def federated_idp_mfa_behavior(self) -> FederatedIdpMfaBehavior:
        """Gets the federatedIdpMfaBehavior property"""
        return self.properties.get("federatedIdpMfaBehavior", FederatedIdpMfaBehavior.acceptIfMfaDoneByFederatedIdp)

    @odata(name="isSignedAuthenticationRequestRequired")
    @property
    def is_signed_authentication_request_required(self) -> Optional[bool]:
        """Gets the isSignedAuthenticationRequestRequired property"""
        return self.properties.get("isSignedAuthenticationRequestRequired", None)

    @odata(name="nextSigningCertificate")
    @property
    def next_signing_certificate(self) -> Optional[str]:
        """Gets the nextSigningCertificate property"""
        return self.properties.get("nextSigningCertificate", None)

    @odata(name="passwordResetUri")
    @property
    def password_reset_uri(self) -> Optional[str]:
        """Gets the passwordResetUri property"""
        return self.properties.get("passwordResetUri", None)

    @odata(name="promptLoginBehavior")
    @property
    def prompt_login_behavior(self) -> PromptLoginBehavior:
        """Gets the promptLoginBehavior property"""
        return self.properties.get("promptLoginBehavior", PromptLoginBehavior.translateToFreshPasswordAuthentication)

    @odata(name="signingCertificateUpdateStatus")
    @property
    def signing_certificate_update_status(self) -> SigningCertificateUpdateStatus:
        """Gets the signingCertificateUpdateStatus property"""
        return self.properties.get("signingCertificateUpdateStatus", SigningCertificateUpdateStatus())

    @odata(name="signOutUri")
    @property
    def sign_out_uri(self) -> Optional[str]:
        """Gets the signOutUri property"""
        return self.properties.get("signOutUri", None)

    @odata(name="systemBrowserEnabledOn")
    @property
    def system_browser_enabled_on(self) -> SystemBrowserEnabledOn:
        """Gets the systemBrowserEnabledOn property"""
        return self.properties.get("systemBrowserEnabledOn", SystemBrowserEnabledOn.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InternalDomainFederation"
