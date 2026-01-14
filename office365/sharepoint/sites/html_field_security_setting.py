from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class HTMLFieldSecuritySetting(ClientValue):
    def __init__(
        self,
        allowed_domains: StringCollection = StringCollection(),
        allow_embedding: int = None,
    ):
        self.allowedDomains = allowed_domains
        self.allowEmbedding = allow_embedding
