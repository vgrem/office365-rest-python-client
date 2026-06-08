from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class PersonalResultSuggestion(ClientValue):
    """The PersonalResultSuggestion complex type contains a personal search result suggestion.

    Args:
        highlighted_title (str): Title of the suggested result. Tokens that match the corresponding personal query MUST be surrounded by the <c0></c0> tags.
        is_best_bet (bool): MUST be true if the suggested result was a best bet for the query.
        title (str): Title of the suggested result.
        url (str): URL of the suggested result.
    """

    HighlightedTitle: str | None = None
    IsBestBet: bool | None = None
    Title: str | None = None
    Url: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.PersonalResultSuggestion"
