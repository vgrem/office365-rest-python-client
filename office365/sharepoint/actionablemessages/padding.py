from office365.runtime.client_value import ClientValue


class Padding(ClientValue):

    def __init__(self, bottom: str = None, left: str = None, right: str = None, top: str = None):
        self.bottom = bottom
        self.left = left
        self.right = right
        self.top = top
