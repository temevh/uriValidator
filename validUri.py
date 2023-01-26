import re


class checkIdentity:
    def __init__(self, uri):
        self.uri = uri
        self.path = None
        self.params = {}
        self.uriChecker()

    def uriChecker(self):
