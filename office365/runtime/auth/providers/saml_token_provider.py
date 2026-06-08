import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional
from xml.dom import minidom
from xml.etree import ElementTree

import requests
import requests.utils
from requests import Response

import office365.logger
from office365.azure_env import AzureEnvironment
from office365.runtime.auth.auth_cookies import AuthCookies
from office365.runtime.auth.authentication_provider import AuthenticationProvider
from office365.runtime.auth.sts_profile import STSProfile
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.auth.user_realm_info import UserRealmInfo
from office365.runtime.http.request_options import RequestOptions

office365.logger.ensure_debug_secrets()


def string_escape(value: str) -> str:
    value = value.replace("&", "&amp;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")
    value = value.replace('"', "&quot;")
    value = value.replace("'", "&apos;")
    return value


def datetime_escape(value: datetime) -> str:
    return value.isoformat("T")[:-9] + "Z"


class SamlTokenProvider(AuthenticationProvider, office365.logger.LoggerContext):
    """SAML Security Token Service provider (claims-based authentication)"""

    def __init__(
        self,
        url,
        credential: UserCredential,
        browser_mode: bool,
        environment: Optional[AzureEnvironment] = None,
    ):
        """SAML Security Token Service provider (claims-based authentication)

        Args:
            url (str): Site or Web absolute url
            credential (UserCredential): User credentials
            browser_mode (bool):
            environment (AzureEnvironment): The Office 365 Cloud Environment endpoint used for authentication.
        """
        # Security Token Service info
        self._sts_profile = STSProfile(url, environment or AzureEnvironment.Global)
        # Obtain authentication cookies, using the browser mode
        self._browser_mode = browser_mode
        # Last occurred error
        self.error = ""
        self._credential = credential
        self._cached_auth_cookies: Optional[AuthCookies] = None
        self.__ns_prefixes = {
            "S": "{http://www.w3.org/2003/05/soap-envelope}",
            "s": "{http://www.w3.org/2003/05/soap-envelope}",
            "psf": "{http://schemas.microsoft.com/Passport/SoapServices/SOAPFault}",
            "wst": "{http://schemas.xmlsoap.org/ws/2005/02/trust}",
            "wsse": "{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}",
            "saml": "{urn:oasis:names:tc:SAML:1.0:assertion}",
            "u": "{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}",
            "wsa": "{http://www.w3.org/2005/08/addressing}",
            "wsp": "{http://schemas.xmlsoap.org/ws/2004/09/policy}",
            "ps": "{http://schemas.microsoft.com/LiveID/SoapServices/v1}",
            "ds": "{http://www.w3.org/2000/09/xmldsig#}",
        }
        for key, prefix in self.__ns_prefixes.items():
            ElementTree.register_namespace(key, prefix[1:-1])

    def authenticate_request(self, request: RequestOptions) -> None:
        """
        Authenticate request handler
        """
        logger = self.logger(self.authenticate_request.__name__)

        request_time = datetime.now(timezone.utc)
        if self._cached_auth_cookies is None or request_time >= self._sts_profile.expires:
            self._sts_profile.reset()
            self._cached_auth_cookies = self.get_authentication_cookie()
        logger.debug_secrets(self._cached_auth_cookies)  # type: ignore[reportAttributeAccessIssue]
        request.set_header("Cookie", self._cached_auth_cookies.cookie_header)

    def get_authentication_cookie(self) -> AuthCookies:
        """Acquire authentication cookie"""
        logger = self.logger(self.get_authentication_cookie.__name__)
        logger.debug("get_authentication_cookie called")

        try:
            logger.debug("Acquiring Access Token..")
            user_realm = self._get_user_realm()
            if user_realm is None:
                raise ValueError("Failed to retrieve user realm information")
            if user_realm.is_federated:
                token = self._acquire_service_token_from_adfs(user_realm.sts_auth_url)  # type: ignore[reportOptionalMemberAccess]
            else:
                token = self._acquire_service_token()
            assert token is not None
            return self._get_authentication_cookie(token, user_realm.is_federated)
        except requests.exceptions.RequestException as e:
            logger.error(e.response.text)  # type: ignore[reportOptionalMemberAccess]
            self.error = f"Error: {e}"
            raise ValueError(e.response.text) from e  # type: ignore[reportOptionalMemberAccess]

    def _get_user_realm(self) -> Optional[UserRealmInfo]:
        """Get User Realm"""
        resp = requests.post(
            self._sts_profile.user_realm_service_url,
            data=f"login={self._credential.userName}&xml=1",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        xml = ElementTree.fromstring(resp.content)
        node = xml.find("NameSpaceType")
        if node is not None:
            if node.text == "Federated":
                sts_auth_url_node = xml.find("STSAuthURL")
                assert sts_auth_url_node is not None and sts_auth_url_node.text is not None
                info = UserRealmInfo(sts_auth_url_node.text, True)
            else:
                info = UserRealmInfo(None, False)
            return info
        return None

    def _acquire_service_token_from_adfs(self, adfs_url: str) -> Optional[str]:
        logger = self.logger(self._acquire_service_token_from_adfs.__name__)

        payload = self._prepare_request_from_template(
            "FederatedSAML.xml",
            {
                "auth_url": adfs_url,
                "message_id": str(uuid.uuid4()),
                "username": string_escape(self._credential.userName),
                "password": string_escape(self._credential.password),
                "created": datetime_escape(self._sts_profile.created),
                "expires": datetime_escape(self._sts_profile.expires),
                "issuer": self._sts_profile.token_issuer,
            },
        )

        response = requests.post(
            adfs_url,
            data=payload,
            headers={"Content-Type": "application/soap+xml; charset=utf-8"},
        )
        dom = minidom.parseString(response.content.decode())
        assertion_node = dom.getElementsByTagNameNS("urn:oasis:names:tc:SAML:1.0:assertion", "Assertion")[0].toxml()

        try:
            payload = self._prepare_request_from_template(
                "RST2.xml",
                {
                    "auth_url": self._sts_profile.tenant,
                    "serviceTokenUrl": self._sts_profile.security_token_service_url,
                    "assertion_node": assertion_node,
                },
            )

            # 3. get security token
            response = requests.post(
                self._sts_profile.security_token_service_url,
                data=payload,
                headers={"Content-Type": "application/soap+xml"},
            )
            token = self._process_service_token_response(response)
            logger.debug_secrets("security token: %s", token)  # type: ignore[reportAttributeAccessIssue]
            return token
        except ElementTree.ParseError as e:
            self.error = f"An error occurred while parsing the server response: {e}"
            logger.error(self.error)
            return None

    def _acquire_service_token(self) -> Optional[str]:
        """Retrieve service token"""
        logger = self.logger(self._acquire_service_token.__name__)

        payload = self._prepare_request_from_template(
            "SAML.xml",
            {
                "auth_url": self._sts_profile.site_url,
                "username": string_escape(self._credential.userName),
                "password": string_escape(self._credential.password),
                "message_id": str(uuid.uuid4()),
                "created": datetime_escape(self._sts_profile.created),
                "expires": datetime_escape(self._sts_profile.expires),
                "issuer": self._sts_profile.token_issuer,
            },
        )
        logger.debug_secrets("options: %s", payload)  # type: ignore[reportAttributeAccessIssue]
        response = requests.post(
            self._sts_profile.security_token_service_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = self._process_service_token_response(response)
        logger.debug_secrets("security token: %s", token)  # type: ignore[reportAttributeAccessIssue]
        return token

    def _process_service_token_response(self, response: Response):
        logger = self.logger(self._process_service_token_response.__name__)
        logger.debug_secrets("response: %s\nresponse.content: %s", response, response.content)  # type: ignore[reportAttributeAccessIssue]

        try:
            xml = ElementTree.fromstring(response.content)
        except ElementTree.ParseError as e:
            self.error = f"An error occurred while parsing the server response: {e}"
            logger.error(self.error)
            return None

        # check for errors
        if xml.find(f"{self.__ns_prefixes['s']}Body/{self.__ns_prefixes['s']}Fault") is not None:
            error = xml.find(
                f"{self.__ns_prefixes['s']}Body/"
                f"{self.__ns_prefixes['s']}Fault/"
                f"{self.__ns_prefixes['s']}Detail/"
                f"{self.__ns_prefixes['psf']}error/"
                f"{self.__ns_prefixes['psf']}internalerror/"
                f"{self.__ns_prefixes['psf']}text"
            )

            if error is None:
                self.error = "An error occurred while retrieving token from XML response."
            else:
                self.error = f"An error occurred while retrieving token from XML response: {error.text}"
            logger.error(self.error)
            raise ValueError(self.error)

        # extract token
        token = xml.find(
            f"{self.__ns_prefixes['s']}Body/"
            f"{self.__ns_prefixes['wst']}RequestSecurityTokenResponse/"
            f"{self.__ns_prefixes['wst']}RequestedSecurityToken/"
            f"{self.__ns_prefixes['wsse']}BinarySecurityToken"
        )

        if token is None:
            self.error = f"Cannot get binary security token for from {self._sts_profile.security_token_service_url}"
            logger.error(self.error)
            raise ValueError(self.error)
        logger.debug_secrets("token: %s", token)  # type: ignore[reportAttributeAccessIssue]
        return token.text

    def _get_authentication_cookie(self, security_token: str, federated: bool = False) -> AuthCookies:
        """Retrieve auth cookie from STS

        Args:
            federated (bool):
            security_token (str):
        """
        logger = self.logger(self._get_authentication_cookie.__name__)

        session = requests.session()
        logger.debug_secrets(  # type: ignore[reportAttributeAccessIssue]
            "session: %s\nsession.post(%s, data=%s)",
            session,
            self._sts_profile.signin_page_url,
            security_token,
        )
        if not federated or self._browser_mode:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            if self._browser_mode:
                headers["User-Agent"] = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"
            session.post(self._sts_profile.signin_page_url, data=security_token, headers=headers)
        else:
            idcrl_endpoint = f"https://{self._sts_profile.tenant}/_vti_bin/idcrl.svc/"
            session.get(
                idcrl_endpoint,
                headers={
                    "User-Agent": "Office365 Python Client",
                    "X-IDCRL_ACCEPTED": "t",
                    "Authorization": f"BPOSIDCRL {security_token}",
                },
            )
        logger.debug_secrets("session.cookies: %s", session.cookies)  # type: ignore[reportAttributeAccessIssue]
        cookies = AuthCookies(requests.utils.dict_from_cookiejar(session.cookies))
        logger.debug_secrets("cookies: %s", cookies)  # type: ignore[reportAttributeAccessIssue]
        if not cookies.is_valid:
            self.error = f"An error occurred while retrieving auth cookies from {self._sts_profile.signin_page_url}"
            logger.error(self.error)
            raise ValueError(self.error)
        return cookies

    def _prepare_request_from_template(self, template_name: str, params: Dict[str, str]) -> str:
        """Construct the request body to acquire security token from STS endpoint"""
        logger = self.logger(self._prepare_request_from_template.__name__)
        logger.debug_secrets("params: %s", params)  # type: ignore[reportAttributeAccessIssue]

        template_path = os.path.join(os.path.dirname(__file__), "templates", template_name)

        with open(template_path, encoding="utf8") as f:
            data = f.read()

        return data.format(**params)
