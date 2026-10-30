from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.organizations.content_customization import ContentCustomization
from office365.intune.organizations.login_page_layout_configuration import LoginPageLayoutConfiguration
from office365.intune.organizations.login_page_text_visibility_settings import LoginPageTextVisibilitySettings
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class OrganizationalBrandingProperties(Entity):
    """
    An abstract type that exposes properties for configuring an organization's branding.

    Organizations can customize their Azure Active Directory (Azure AD) sign-in pages which appear when users sign in to
    their organization's tenant-specific apps, or when Azure AD identifies the user's tenant from their username.
    A developer can also read the company's branding information and customize their app experience to tailor
    it specifically for the signed-in user using their company's branding.

    You can't change your original configuration's language as represented by the organizationalBranding object.
    However, companies can add different branding based on locale. For language-specific branding,
    see the organizationalBrandingLocalization object.
    """

    @odata(name="backgroundColor")
    @property
    def background_color(self) -> Optional[str]:
        """Gets the backgroundColor property"""
        return self.properties.get("backgroundColor", None)

    @odata(name="backgroundImage")
    @property
    def background_image(self) -> Optional[bytes]:
        """Gets the backgroundImage property"""
        return self.properties.get("backgroundImage", None)

    @odata(name="backgroundImageRelativeUrl")
    @property
    def background_image_relative_url(self) -> Optional[str]:
        """Gets the backgroundImageRelativeUrl property"""
        return self.properties.get("backgroundImageRelativeUrl", None)

    @odata(name="bannerLogo")
    @property
    def banner_logo(self) -> Optional[bytes]:
        """Gets the bannerLogo property"""
        return self.properties.get("bannerLogo", None)

    @odata(name="bannerLogoRelativeUrl")
    @property
    def banner_logo_relative_url(self) -> Optional[str]:
        """Gets the bannerLogoRelativeUrl property"""
        return self.properties.get("bannerLogoRelativeUrl", None)

    @odata(name="cdnList")
    @property
    def cdn_list(self) -> StringCollection:
        """Gets the cdnList property"""
        return self.properties.get("cdnList", StringCollection())

    @odata(name="contentCustomization")
    @property
    def content_customization(self) -> ContentCustomization:
        """Gets the contentCustomization property"""
        return self.properties.get("contentCustomization", ContentCustomization())

    @odata(name="customAccountResetCredentialsUrl")
    @property
    def custom_account_reset_credentials_url(self) -> Optional[str]:
        """Gets the customAccountResetCredentialsUrl property"""
        return self.properties.get("customAccountResetCredentialsUrl", None)

    @odata(name="customCannotAccessYourAccountText")
    @property
    def custom_cannot_access_your_account_text(self) -> Optional[str]:
        """Gets the customCannotAccessYourAccountText property"""
        return self.properties.get("customCannotAccessYourAccountText", None)

    @odata(name="customCannotAccessYourAccountUrl")
    @property
    def custom_cannot_access_your_account_url(self) -> Optional[str]:
        """Gets the customCannotAccessYourAccountUrl property"""
        return self.properties.get("customCannotAccessYourAccountUrl", None)

    @odata(name="customCSS")
    @property
    def custom_css(self) -> Optional[bytes]:
        """Gets the customCSS property"""
        return self.properties.get("customCSS", None)

    @odata(name="customCSSRelativeUrl")
    @property
    def custom_css_relative_url(self) -> Optional[str]:
        """Gets the customCSSRelativeUrl property"""
        return self.properties.get("customCSSRelativeUrl", None)

    @odata(name="customForgotMyPasswordText")
    @property
    def custom_forgot_my_password_text(self) -> Optional[str]:
        """Gets the customForgotMyPasswordText property"""
        return self.properties.get("customForgotMyPasswordText", None)

    @odata(name="customPrivacyAndCookiesText")
    @property
    def custom_privacy_and_cookies_text(self) -> Optional[str]:
        """Gets the customPrivacyAndCookiesText property"""
        return self.properties.get("customPrivacyAndCookiesText", None)

    @odata(name="customPrivacyAndCookiesUrl")
    @property
    def custom_privacy_and_cookies_url(self) -> Optional[str]:
        """Gets the customPrivacyAndCookiesUrl property"""
        return self.properties.get("customPrivacyAndCookiesUrl", None)

    @odata(name="customResetItNowText")
    @property
    def custom_reset_it_now_text(self) -> Optional[str]:
        """Gets the customResetItNowText property"""
        return self.properties.get("customResetItNowText", None)

    @odata(name="customTermsOfUseText")
    @property
    def custom_terms_of_use_text(self) -> Optional[str]:
        """Gets the customTermsOfUseText property"""
        return self.properties.get("customTermsOfUseText", None)

    @odata(name="customTermsOfUseUrl")
    @property
    def custom_terms_of_use_url(self) -> Optional[str]:
        """Gets the customTermsOfUseUrl property"""
        return self.properties.get("customTermsOfUseUrl", None)

    @odata(name="favicon")
    @property
    def favicon(self) -> Optional[bytes]:
        """Gets the favicon property"""
        return self.properties.get("favicon", None)

    @odata(name="faviconRelativeUrl")
    @property
    def favicon_relative_url(self) -> Optional[str]:
        """Gets the faviconRelativeUrl property"""
        return self.properties.get("faviconRelativeUrl", None)

    @odata(name="headerBackgroundColor")
    @property
    def header_background_color(self) -> Optional[str]:
        """Gets the headerBackgroundColor property"""
        return self.properties.get("headerBackgroundColor", None)

    @odata(name="headerLogo")
    @property
    def header_logo(self) -> Optional[bytes]:
        """Gets the headerLogo property"""
        return self.properties.get("headerLogo", None)

    @odata(name="headerLogoRelativeUrl")
    @property
    def header_logo_relative_url(self) -> Optional[str]:
        """Gets the headerLogoRelativeUrl property"""
        return self.properties.get("headerLogoRelativeUrl", None)

    @odata(name="loginPageLayoutConfiguration")
    @property
    def login_page_layout_configuration(self) -> LoginPageLayoutConfiguration:
        """Gets the loginPageLayoutConfiguration property"""
        return self.properties.get("loginPageLayoutConfiguration", LoginPageLayoutConfiguration())

    @odata(name="loginPageTextVisibilitySettings")
    @property
    def login_page_text_visibility_settings(self) -> LoginPageTextVisibilitySettings:
        """Gets the loginPageTextVisibilitySettings property"""
        return self.properties.get("loginPageTextVisibilitySettings", LoginPageTextVisibilitySettings())

    @odata(name="signInPageText")
    @property
    def sign_in_page_text(self) -> Optional[str]:
        """Gets the signInPageText property"""
        return self.properties.get("signInPageText", None)

    @odata(name="squareLogo")
    @property
    def square_logo(self) -> Optional[bytes]:
        """Gets the squareLogo property"""
        return self.properties.get("squareLogo", None)

    @odata(name="squareLogoDark")
    @property
    def square_logo_dark(self) -> Optional[bytes]:
        """Gets the squareLogoDark property"""
        return self.properties.get("squareLogoDark", None)

    @odata(name="squareLogoDarkRelativeUrl")
    @property
    def square_logo_dark_relative_url(self) -> Optional[str]:
        """Gets the squareLogoDarkRelativeUrl property"""
        return self.properties.get("squareLogoDarkRelativeUrl", None)

    @odata(name="squareLogoRelativeUrl")
    @property
    def square_logo_relative_url(self) -> Optional[str]:
        """Gets the squareLogoRelativeUrl property"""
        return self.properties.get("squareLogoRelativeUrl", None)

    @odata(name="usernameHintText")
    @property
    def username_hint_text(self) -> Optional[str]:
        """Gets the usernameHintText property"""
        return self.properties.get("usernameHintText", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OrganizationalBrandingProperties"
