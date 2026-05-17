# Authentication Examples

This directory contains examples demonstrating various authentication flows for Microsoft Graph using the `office365-rest-python-client` library.

## Examples

| File | Authentication Flow |
|---|---|
| [interactive.py](interactive.py) | Interactive browser login (built-in) |
| [interactive_custom.py](interactive_custom.py) | Interactive browser login (custom callback) |
| [with_client_secret.py](with_client_secret.py) | Client secret (application-only, built-in) |
| [with_client_secret_custom.py](with_client_secret_custom.py) | Client secret (application-only, custom callback) |
| [with_client_cert.py](with_client_cert.py) | Client certificate (X.509) |
| [with_user_creds.py](with_user_creds.py) | Username/password ROPC flow (built-in) |
| [with_user_creds_custom.py](with_user_creds_custom.py) | Username/password ROPC flow (custom callback) |
| [with_adal.py](with_adal.py) | Legacy ADAL library (username/password) |
| [gcc_high.py](gcc_high.py) | GCC High national cloud |

## Prerequisites

- Python 3.8+
- Azure AD app registration with appropriate permissions
- Credentials configured in `tests` package (client_id, tenant, secret, etc.)

## Documentation

- [Microsoft Graph authentication overview](https://learn.microsoft.com/en-us/graph/auth)
- [Microsoft identity platform authentication flows](https://learn.microsoft.com/en-us/azure/active-directory/develop/msal-authentication-flows)
