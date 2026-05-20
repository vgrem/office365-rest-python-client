from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SubwebQuery(ClientValue):
    """Defines a query to specify which child Web sites to return from a Web site.

    ConfigurationFilter: A 16-bit integer that specifies the identifier of a configuration
    WebTemplateFilter: Specifies the site definition.
    """

    ConfigurationFilter: int = -1
    WebTemplateFilter: int = -1
