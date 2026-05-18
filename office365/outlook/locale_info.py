from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class LocaleInfo(ClientValue):
    """Information about the locale, including the preferred language and country/region, of the signed-in user.

    Fields:
        displayName (str | None): A name representing the user's locale in natural language,
            for example, "English (United States)".
        locale (str | None): A locale representation for the user, which includes the user's preferred language
            and country/region. For example, "en-us". The language component follows 2-letter codes as defined in
            ISO 639-1, and the country component follows 2-letter codes as defined in ISO 3166-1 alpha-2.
    """

    displayName: str | None = None
    locale: str | None = None

    def __repr__(self):
        return self.locale or ""
