import base64
import hashlib
import json
import threading
import time
import logging
import warnings

from .authority import canonicalize
from .oauth2cli.oidc import decode_part, _decode_id_token_claims
from .oauth2cli.oauth2 import Client


logger = logging.getLogger(__name__)
_GRANT_TYPE_BROKER = "broker"

# Fields in the request data dict that should NOT be included in the extended
# cache key hash. Everything else in data IS included, because those are extra
# body parameters going on the wire and must differentiate cached tokens.
#
# Excluded fields and reasons:
#   - "client_id"              : Standard OAuth2 client identifier, same for every request
#   - "grant_type"             : It is possible to combine grants to get tokens, e.g. obo + refresh_token, auth_code + refresh_token etc.
#   - "scope"                  : Already represented as "target" in the AT cache key
#   - "claims"                 : Handled separately; its presence forces a token refresh
#   - "username"               : Standard ROPC grant parameter. Tokens are cached by user ID (subject or oid+tid) instead
#   - "password"               : Standard ROPC grant parameter. Tokens are tied to credentials.
#   - "refresh_token"          : Standard refresh grant parameter
#   - "code"                   : Standard authorization code grant parameter
#   - "redirect_uri"           : Standard authorization code grant parameter
#   - "code_verifier"          : Standard PKCE parameter
#   - "device_code"            : Standard device flow parameter
#   - "assertion"              : Standard OBO/SAML assertion (RFC 7521)
#   - "requested_token_use"    : OBO indicator ("on_behalf_of"), not an extra param
#   - "client_assertion"       : Client authentication credential (RFC 7521 §4.2)
#   - "client_assertion_type"  : Client authentication type (RFC 7521 §4.2)
#   - "client_secret"          : Client authentication secret
#   - "token_type"             : Used for SSH-cert/POP detection; AT entry stores separately
#   - "req_cnf"                : Ephemeral proof-of-possession nonce, changes per request
#   - "key_id"                 : Already handled as a separate cache lookup field
#
# Included fields (examples — anything NOT in this set is included):
#   - "fmi_path"               : Federated Managed Identity credential path
#   - any future non-standard body parameter that should isolate cache entries
_EXT_CACHE_KEY_EXCLUDED_FIELDS = frozenset({
    # Standard OAuth2 body parameters — these appear in every token request
    # and must NOT influence the extended cache key.
    # Only non-standard fields (e.g. fmi_path) should contribute to the hash.
    "client_id",
    "grant_type",
    "scope",
    "claims",
    "username",
    "password",
    "refresh_token",
    "code",
    "redirect_uri",
    "code_verifier",
    "device_code",
    "assertion",
    "requested_token_use",
    "client_assertion",
    "client_assertion_type",
    "client_secret",
    "token_type",
    "req_cnf",
    "key_id",
    # user_fic grant parameters — these are standard body params for the
    # user_fic flow; FIC tokens use normal user cache keys (not extended).
    "user_federated_identity_credential",
    "user_id",
    "client_info",
})


def _compute_ext_cache_key(data):
    """Compute an extended cache key hash from extra body parameters in *data*.

    All fields in *data* that go on the wire are included in the hash,
    EXCEPT those listed in ``_EXT_CACHE_KEY_EXCLUDED_FIELDS``.
    This ensures tokens acquired with different parameter values
    (e.g., different FMI paths) are cached separately.

    The hash may also intentionally include cache-key-only pseudo-parameters
    such as ``client_claims`` -- these are stripped from the wire body by the
    oauth2 layer but are retained in *data* precisely so that different
    client-originated claims route to separate cache entries.

    Returns an empty string when *data* has no hashable fields.

    The algorithm uses a length-prefixed ("netstring") serialization matching
    MSAL Go's ``CacheExtKeyGenerator``
    (AzureAD/microsoft-authentication-library-for-go#629): for each key sorted
    ascending, ``<byteLen(key)>:<key><byteLen(value)>:<value>`` is appended and
    the parts concatenated, then SHA256 hashed and base64url (no padding)
    encoded and lowercased.

    The length prefixes make the *serialization* injective: distinct component
    sets can never produce the same pre-hash string, so they cannot collide at
    the serialization layer. (The final cache key is still a SHA-256 digest, so
    only a cryptographically negligible hash collision remains possible.) A plain
    ``key + value`` concatenation, by contrast, is ambiguous: ``{"fmi_path":
    "value"}`` and ``{"fmi_pat": "hvalue"}`` would both serialize to
    ``fmi_pathvalue``. The byte length (``len(s.encode("utf-8"))``), not the
    Unicode code-point count, is used so the hash stays byte-identical across the
    MSAL SDK family (Go/.NET/Java/JS) as they converge on this scheme.
    """
    if not data:
        return ""
    cache_components = {
        k: str(v) for k, v in data.items()
        if k not in _EXT_CACHE_KEY_EXCLUDED_FIELDS and v
    }
    if not cache_components:
        return ""
    # Sort keys, then length-prefix each key and value so the serialization is
    # injective (see docstring). Byte-identical to MSAL Go's netstring encoding.
    key_str = "".join(
        "{klen}:{k}{vlen}:{v}".format(
            klen=len(k.encode("utf-8")), k=k,
            vlen=len(cache_components[k].encode("utf-8")), v=cache_components[k])
        for k in sorted(cache_components.keys())
    )
    hash_bytes = hashlib.sha256(key_str.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(hash_bytes).rstrip(b"=").decode("ascii").lower()


def _parse_claims_or_raise(claims):
    """Parse a claims JSON string into a dict, or raise a friendly ``ValueError``.

    The raw claims value is never included in the error message because it may
    contain sensitive data. Mirrors MSAL .NET's ``ClaimsHelper.ParseClaimsOrThrow``.
    """
    try:
        parsed = json.loads(claims)
    except (ValueError, TypeError) as ex:
        # json.JSONDecodeError (malformed JSON) is a subclass of ValueError;
        # TypeError is raised when *claims* is not a str/bytes/bytearray. Both
        # are surfaced as the same friendly ValueError so every caller behaves
        # consistently regardless of the bad input's type.
        raise ValueError(
            "The claims value is not valid JSON. "
            "See https://openid.net/specs/openid-connect-core-1_0.html#ClaimsParameter."
        ) from ex
    if not isinstance(parsed, dict):
        # A valid JSON array, scalar, or the literal "null" is not a claims object.
        raise ValueError(
            "The claims value is not a valid JSON object. "
            "See https://openid.net/specs/openid-connect-core-1_0.html#ClaimsParameter.")
    return parsed


def _deep_merge_dict(base, overlay):
    """Recursively merge ``overlay`` into ``base``, returning a new dict.

    Nested dicts are merged; for any other value type, ``overlay`` wins.
    """
    result = dict(base)
    for key, value in overlay.items():
        if (key in result
                and isinstance(result[key], dict) and isinstance(value, dict)):
            result[key] = _deep_merge_dict(result[key], value)
        else:
            result[key] = value
    return result


def _merge_claims(claims_a, claims_b):
    """Merge two claims JSON strings into a single JSON string.

    If either side is empty/None, the other is returned as-is. Mirrors MSAL
    .NET's ``ClaimsHelper.MergeClaimsObjects``.
    """
    if not claims_a:
        return claims_b
    if not claims_b:
        return claims_a
    merged = _deep_merge_dict(
        _parse_claims_or_raise(claims_a), _parse_claims_or_raise(claims_b))
    return json.dumps(merged)


def is_subdict_of(small, big):
    return dict(big, **small) == big

def _get_username(id_token_claims):
    return id_token_claims.get(
        "preferred_username",  # AAD
        id_token_claims.get("upn"))  # ADFS 2019

class TokenCache(object):
    """This is considered as a base class containing minimal cache behavior.

    Although it maintains tokens using unified schema across all MSAL libraries,
    this class does not serialize/persist them.
    See subclass :class:`SerializableTokenCache` for details on serialization.
    """

    class CredentialType:
        ACCESS_TOKEN = "AccessToken"
        ACCESS_TOKEN_EXTENDED = "atext"  # Used when ext_cache_key is present (matches Go/dotnet)
        REFRESH_TOKEN = "RefreshToken"
        ACCOUNT = "Account"  # Not exactly a credential type, but we put it here
        ID_TOKEN = "IdToken"
        APP_METADATA = "AppMetadata"

    class AuthorityType:
        ADFS = "ADFS"
        MSSTS = "MSSTS"  # MSSTS means AAD v2 for both AAD & MSA

    def __init__(self):
        self._lock = threading.RLock()
        self._cache = {}
        self.key_makers = {
            # Note: We have changed token key format before when ordering scopes;
            #       changing token key won't result in cache miss.
            self.CredentialType.REFRESH_TOKEN:
                lambda home_account_id=None, environment=None, client_id=None,
                        target=None, **ignored_payload_from_a_real_token:
                    "-".join([
                        home_account_id or "",
                        environment or "",
                        self.CredentialType.REFRESH_TOKEN,
                        client_id or "",
                        "",  # RT is cross-tenant in AAD
                        target or "",  # raw value could be None if deserialized from other SDK
                        ]).lower(),
            self.CredentialType.ACCESS_TOKEN:
                lambda home_account_id=None, environment=None, client_id=None,
                        realm=None, target=None,
                        ext_cache_key=None,
                        # Note: New field(s) can be added here
                        #key_id=None,
                        **ignored_payload_from_a_real_token:
                    "-".join([  # Note: Could use a hash here to shorten key length
                        home_account_id or "",
                        environment or "",
                        # Use "atext" credential type when ext_cache_key is
                        # present, matching MSAL Go and MSAL .NET behaviour.
                        "atext" if ext_cache_key else "AccessToken",
                        client_id or "",
                        realm or "",
                        target or "",
                        #key_id or "",  # So ATs of different key_id can coexist
                        ] + ([ext_cache_key] if ext_cache_key else [])
                        ).lower(),
            self.CredentialType.ID_TOKEN:
                lambda home_account_id=None, environment=None, client_id=None,
                        realm=None, **ignored_payload_from_a_real_token:
                    "-".join([
                        home_account_id or "",
                        environment or "",
                        self.CredentialType.ID_TOKEN,
                        client_id or "",
                        realm or "",
                        ""  # Albeit irrelevant, schema requires an empty scope here
                        ]).lower(),
            self.CredentialType.ACCOUNT:
                lambda home_account_id=None, environment=None, realm=None,
                        **ignored_payload_from_a_real_entry:
                    "-".join([
                        home_account_id or "",
                        environment or "",
                        realm or "",
                        ]).lower(),
            self.CredentialType.APP_METADATA:
                lambda environment=None, client_id=None, **kwargs:
                    "appmetadata-{}-{}".format(environment or "", client_id or ""),
            }

    def _get_access_token(
        self,
        home_account_id, environment, client_id, realm, target,  # Together they form a compound key
        ext_cache_key=None,
        default=None,
    ):  # O(1)
        return self._get(
            self.CredentialType.ACCESS_TOKEN,
            self.key_makers[TokenCache.CredentialType.ACCESS_TOKEN](
                home_account_id=home_account_id,
                environment=environment,
                client_id=client_id,
                realm=realm,
                target=" ".join(target),
                ext_cache_key=ext_cache_key,
                ),
            default=default)

    def _get_app_metadata(self, environment, client_id, default=None):  # O(1)
        return self._get(
            self.CredentialType.APP_METADATA,
            self.key_makers[TokenCache.CredentialType.APP_METADATA](
                environment=environment,
                client_id=client_id,
                ),
            default=default)

    def _get(self, credential_type, key, default=None):  # O(1)
        with self._lock:
            return self._cache.get(credential_type, {}).get(key, default)

    @staticmethod
    def _is_matching(entry: dict, query: dict, target_set: set = None) -> bool:
        query_with_lowercase_environment = {
            # __add() canonicalized entry's environment value to lower case,
            # so we do the same here.
            k: v.lower() if k == "environment" and isinstance(v, str) else v
            for k, v in query.items()
        } if query else {}
        return is_subdict_of(query_with_lowercase_environment, entry) and (
            target_set <= set(entry.get("target", "").split())
            if target_set else True)

    def search(self, credential_type, target=None, query=None, *, now=None):  # O(n) generator
        """Returns a generator of matching entries.

        It is O(1) for AT hits, and O(n) for other types.
        Note that it holds a lock during the entire search.
        """
        target = sorted(target or [])  # Match the order sorted by add()
        assert isinstance(target, list), "Invalid parameter type"

        preferred_result = None
        if (credential_type == self.CredentialType.ACCESS_TOKEN
            and isinstance(query, dict)
            and "home_account_id" in query and "environment" in query
            and "client_id" in query and "realm" in query and target
        ):  # Special case for O(1) AT lookup
            preferred_result = self._get_access_token(
                query["home_account_id"], query["environment"],
                query["client_id"], query["realm"], target,
                ext_cache_key=query.get("ext_cache_key"))
            if preferred_result and self._is_matching(
                preferred_result, query,
                # Needs no target_set here because it is satisfied by dict key
            ):
                yield preferred_result

        target_set = set(target)
        with self._lock:
            # O(n) search. The key is NOT used in search.
            now = int(time.time() if now is None else now)
            expired_access_tokens = [
                # Especially when/if we key ATs by ephemeral fields such as key_id,
                # stale ATs keyed by an old key_id would stay forever.
                # Here we collect them for their removal.
            ]
            for entry in self._cache.get(credential_type, {}).values():
                if (  # Automatically delete expired access tokens
                    credential_type == self.CredentialType.ACCESS_TOKEN
                    and int(entry["expires_on"]) < now
                ):
                    expired_access_tokens.append(entry)  # Can't delete them within current for-loop
                    continue
                if (entry != preferred_result  # Avoid yielding the same entry twice
                    and self._is_matching(entry, query, target_set=target_set)
                ):
                    # Cache isolation for extended cache keys (e.g., FMI path).
                    # Entries with ext_cache_key must not match queries without one.
                    if (credential_type == self.CredentialType.ACCESS_TOKEN
                        and "ext_cache_key" in entry
                        and "ext_cache_key" not in (query or {})
                    ):
                        continue
                    yield entry
            for at in expired_access_tokens:
                self.remove_at(at)

    def find(self, credential_type, target=None, query=None, *, now=None):
        """Equivalent to list(search(...))."""
        warnings.warn(
            "Use list(search(...)) instead to explicitly get a list.",
            DeprecationWarning)
        return list(self.search(credential_type, target=target, query=query, now=now))

    def add(self, event, now=None):
        """Handle a token obtaining event, and add tokens into cache."""
        def make_clean_copy(dictionary, sensitive_fields):  # Masks sensitive info
            return {
                k: "********" if k in sensitive_fields else v
                for k, v in dictionary.items()
            }
        clean_event = dict(
            event,
            data=make_clean_copy(event.get("data", {}), (
                "password", "client_secret", "refresh_token", "assertion",
                "user_federated_identity_credential",
                # Client-originated claims may carry sensitive values; they are
                # kept in data only for ext_cache_key computation, so redact them
                # from the debug log (both the cache-key pseudo-param and the
                # merged wire parameter).
                "client_claims", "claims",
            )),
            response=make_clean_copy(event.get("response", {}), (
                "id_token_claims",  # Provided by broker
                "access_token", "refresh_token", "id_token", "username",
            )),
        )
        logger.debug("event=%s", json.dumps(
        # We examined and concluded that this log won't have Log Injection risk,
        # because the event payload is already in JSON so CR/LF will be escaped.
            clean_event,
            indent=4, sort_keys=True,
            default=str,  # assertion is in bytes in Python 3
        ))
        return self.__add(event, now=now)

    def __parse_account(self, response, id_token_claims):
        """Return client_info and home_account_id"""
        if "client_info" in response:  # It happens when client_info and profile are in request
            client_info = json.loads(decode_part(response["client_info"]))
            if "uid" in client_info and "utid" in client_info:
                return client_info, "{uid}.{utid}".format(**client_info)
            # https://github.com/AzureAD/microsoft-authentication-library-for-python/issues/387
        if id_token_claims:  # This would be an end user on ADFS-direct scenario
            sub = id_token_claims["sub"]  # "sub" always exists, per OIDC specs
            return {"uid": sub}, sub
        # client_credentials flow will reach this code path
        return {}, None

    def __add(self, event, now=None):
        # event typically contains: client_id, scope, token_endpoint,
        # response, params, data, grant_type
        environment = realm = None
        if "token_endpoint" in event:
            _, environment, realm = canonicalize(event["token_endpoint"])
        if "environment" in event:  # Always available unless in legacy test cases
            environment = event["environment"]  # Set by application.py
        response = event.get("response", {})
        data = event.get("data", {})
        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")
        id_token = response.get("id_token")
        id_token_claims = response.get("id_token_claims") or (  # Prefer the claims from broker
            # MSAL does not validate the ID token; it only decodes the claims.
            # https://github.com/AzureAD/microsoft-authentication-library-for-python/issues/911
            _decode_id_token_claims(id_token) if id_token else {})
        client_info, home_account_id = self.__parse_account(response, id_token_claims)

        target = ' '.join(sorted(event.get("scope") or []))  # Schema should have required sorting

        with self._lock:
            now = int(time.time() if now is None else now)

            if access_token:
                default_expires_in = (  # https://www.rfc-editor.org/rfc/rfc6749#section-5.1
                    int(response.get("expires_on")) - now  # Some Managed Identity emits this
                    ) if response.get("expires_on") else 600
                expires_in = int(  # AADv1-like endpoint returns a string
                    response.get("expires_in", default_expires_in))
                ext_expires_in = int(  # AADv1-like endpoint returns a string
			response.get("ext_expires_in", expires_in))
                at = {
                    "credential_type": self.CredentialType.ACCESS_TOKEN,
                    "secret": access_token,
                    "home_account_id": home_account_id,
                    "environment": environment,
                    "client_id": event.get("client_id"),
                    "target": target,
                    "realm": realm,
                    "token_type": response.get("token_type", "Bearer"),
                    "cached_at": str(now),  # Schema defines it as a string
                    "expires_on": str(now + expires_in),  # Same here
                    "extended_expires_on": str(now + ext_expires_in)  # Same here
                    }
                at.update({k: data[k] for k in data if k in {
                    # Also store extra data which we explicitly allow
                    # So that we won't accidentally store a user's password etc.
                    "key_id",  # It happens in SSH-cert or POP scenario
                }})
                # Compute and store extended cache key for cache isolation
                # (e.g., different FMI paths should have separate cache entries)
                ext_cache_key = _compute_ext_cache_key(data)
                
                if ext_cache_key:
                    at["ext_cache_key"] = ext_cache_key
                if "refresh_in" in response:
                    refresh_in = response["refresh_in"]  # It is an integer
                    at["refresh_on"] = str(now + refresh_in)  # Schema wants a string
                self.modify(self.CredentialType.ACCESS_TOKEN, at, at)

            if client_info and not event.get("skip_account_creation"):
                account = {
                    "home_account_id": home_account_id,
                    "environment": environment,
                    "realm": realm,
                    "local_account_id": event.get(
                        "_account_id",  # Came from mid-tier code path.
                            # Emperically, it is the oid in AAD or cid in MSA.
                        id_token_claims.get("oid", id_token_claims.get("sub"))),
                    "username": _get_username(id_token_claims)
                        or data.get("username")  # Falls back to ROPC username
                        or event.get("username")  # Falls back to Federated ROPC username
                        or "",  # The schema does not like null
                    "authority_type": event.get(
                        "authority_type",  # Honor caller's choice of authority_type
                        self.AuthorityType.ADFS if realm == "adfs"
                            else self.AuthorityType.MSSTS),
                    # "client_info": response.get("client_info"),  # Optional
                    }
                grant_types_that_establish_an_account = (
                    _GRANT_TYPE_BROKER, "authorization_code", "password",
                    Client.DEVICE_FLOW["GRANT_TYPE"], "user_fic")
                if event.get("grant_type") in grant_types_that_establish_an_account:
                    account["account_source"] = event["grant_type"]
                self.modify(self.CredentialType.ACCOUNT, account, account)

            if id_token:
                idt = {
                    "credential_type": self.CredentialType.ID_TOKEN,
                    "secret": id_token,
                    "home_account_id": home_account_id,
                    "environment": environment,
                    "realm": realm,
                    "client_id": event.get("client_id"),
                    # "authority": "it is optional",
                    }
                self.modify(self.CredentialType.ID_TOKEN, idt, idt)

            if refresh_token:
                rt = {
                    "credential_type": self.CredentialType.REFRESH_TOKEN,
                    "secret": refresh_token,
                    "home_account_id": home_account_id,
                    "environment": environment,
                    "client_id": event.get("client_id"),
                    "target": target,  # Optional per schema though
                    "last_modification_time": str(now),  # Optional. Schema defines it as a string.
                    }
                if "foci" in response:
                    rt["family_id"] = response["foci"]
                self.modify(self.CredentialType.REFRESH_TOKEN, rt, rt)

            app_metadata = {
                "client_id": event.get("client_id"),
                "environment": environment,
                }
            if "foci" in response:
                app_metadata["family_id"] = response.get("foci")
            self.modify(self.CredentialType.APP_METADATA, app_metadata, app_metadata)

    def modify(self, credential_type, old_entry, new_key_value_pairs=None):
        # Modify the specified old_entry with new_key_value_pairs,
        # or remove the old_entry if the new_key_value_pairs is None.

        # This helper exists to consolidate all token add/modify/remove behaviors,
        # so that the sub-classes will have only one method to work on,
        # instead of patching a pair of update_xx() and remove_xx() per type.
        # You can monkeypatch self.key_makers to support more types on-the-fly.
        key = self.key_makers[credential_type](**old_entry)
        with self._lock:
            if new_key_value_pairs:  # Update with them
                entries = self._cache.setdefault(credential_type, {})
                entries[key] = dict(
                    old_entry,  # Do not use entries[key] b/c it might not exist
                    **new_key_value_pairs)
            else:  # Remove old_entry
                self._cache.setdefault(credential_type, {}).pop(key, None)

    def remove_rt(self, rt_item):
        assert rt_item.get("credential_type") == self.CredentialType.REFRESH_TOKEN
        return self.modify(self.CredentialType.REFRESH_TOKEN, rt_item)

    def update_rt(self, rt_item, new_rt):
        assert rt_item.get("credential_type") == self.CredentialType.REFRESH_TOKEN
        return self.modify(self.CredentialType.REFRESH_TOKEN, rt_item, {
            "secret": new_rt,
            "last_modification_time": str(int(time.time())),  # Optional. Schema defines it as a string.
            })

    def remove_at(self, at_item):
        assert at_item.get("credential_type") == self.CredentialType.ACCESS_TOKEN
        return self.modify(self.CredentialType.ACCESS_TOKEN, at_item)

    def remove_idt(self, idt_item):
        assert idt_item.get("credential_type") == self.CredentialType.ID_TOKEN
        return self.modify(self.CredentialType.ID_TOKEN, idt_item)

    def remove_account(self, account_item):
        assert "authority_type" in account_item
        return self.modify(self.CredentialType.ACCOUNT, account_item)


class SerializableTokenCache(TokenCache):
    """This serialization can be a starting point to implement your own persistence.

    This class does NOT actually persist the cache on disk/db/etc..
    Depending on your need,
    the following simple recipe for file-based, unencrypted persistence may be sufficient::

        import os, atexit, msal
        cache_filename = os.path.join(  # Persist cache into this file
            os.getenv(
                # Automatically wipe out the cache from Linux when user's ssh session ends.
                # See also https://github.com/AzureAD/microsoft-authentication-library-for-python/issues/690
                "XDG_RUNTIME_DIR", ""),
            "my_cache.bin")
        cache = msal.SerializableTokenCache()
        if os.path.exists(cache_filename):
            cache.deserialize(open(cache_filename, "r").read())
        atexit.register(lambda:
            open(cache_filename, "w").write(cache.serialize())
            # Hint: The following optional line persists only when state changed
            if cache.has_state_changed else None
            )
        app = msal.ClientApplication(..., token_cache=cache)
        ...

    Alternatively, you may use a more sophisticated cache persistence library,
    `MSAL Extensions <https://github.com/AzureAD/microsoft-authentication-extensions-for-python>`_,
    which provides token cache persistence with encryption, and more.

    :var bool has_state_changed:
        Indicates whether the cache state in the memory has changed since last
        :func:`~serialize` or :func:`~deserialize` call.
    """
    has_state_changed = False

    def add(self, event, **kwargs):
        super(SerializableTokenCache, self).add(event, **kwargs)
        self.has_state_changed = True

    def modify(self, credential_type, old_entry, new_key_value_pairs=None):
        super(SerializableTokenCache, self).modify(
            credential_type, old_entry, new_key_value_pairs)
        self.has_state_changed = True

    def deserialize(self, state):
        # type: (Optional[str]) -> None
        """Deserialize the cache from a state previously obtained by serialize()"""
        with self._lock:
            self._cache = json.loads(state) if state else {}
            self.has_state_changed = False  # reset

    def serialize(self):
        # type: () -> str
        """Serialize the current cache state into a string."""
        with self._lock:
            self.has_state_changed = False
            return json.dumps(self._cache, indent=4)

