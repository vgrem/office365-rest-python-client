from office365.runtime.client_value import ClientValue


class OnPremisesExtensionAttributes(ClientValue):
    def __init__(
        self,
        extension_attribute1: str = None,
        extension_attribute10: str = None,
        extension_attribute11: str = None,
        extension_attribute12: str = None,
        extension_attribute13: str = None,
        extension_attribute14: str = None,
        extension_attribute15: str = None,
        extension_attribute2: str = None,
        extension_attribute3: str = None,
        extension_attribute4: str = None,
        extension_attribute5: str = None,
        extension_attribute6: str = None,
        extension_attribute7: str = None,
        extension_attribute8: str = None,
        extension_attribute9: str = None,
    ):
        self.extensionAttribute1 = extension_attribute1
        self.extensionAttribute10 = extension_attribute10
        self.extensionAttribute11 = extension_attribute11
        self.extensionAttribute12 = extension_attribute12
        self.extensionAttribute13 = extension_attribute13
        self.extensionAttribute14 = extension_attribute14
        self.extensionAttribute15 = extension_attribute15
        self.extensionAttribute2 = extension_attribute2
        self.extensionAttribute3 = extension_attribute3
        self.extensionAttribute4 = extension_attribute4
        self.extensionAttribute5 = extension_attribute5
        self.extensionAttribute6 = extension_attribute6
        self.extensionAttribute7 = extension_attribute7
        self.extensionAttribute8 = extension_attribute8
        self.extensionAttribute9 = extension_attribute9

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnPremisesExtensionAttributes"
