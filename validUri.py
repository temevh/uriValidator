import re
from urllib.parse import urlparse


class checkIdentity:
    def __init__(self, uri):
        self.uri = uri
        self.path = None
        self.params = {}
        self.uriChecker()

    def uriChecker(self):
        isValid = re.match("^visma-identity://.*", self.uri)
        if isValid:
            print("URL IS VALID")
            parsed_uri = urlparse(self.uri)
            self.path = parsed_uri.netloc
            print(self.path)

        else:
            raise Exception("Check URI scheme")

        if self.path not in ['login', 'confirm', 'sign']:
            raise Exception("Check URI path")

        parameters = re.search(r'\?(.*)', self.uri).group(1)
        for p in parameters.split("&"):
            key, value = p.split("=")
            self.params[key] = value

        if self.path == "login":
            if "source" not in self.params:
                raise Exception("Check source parameter")
        elif self.path == "confirm":
            if "source" not in self.params or "paymentnumber" not in self.params:
                raise Exception(
                    "Check source and/or paymentnumber parameter(s)")
            if not self.params["paymentnumber"].isdigit():
                raise Exception("Check paymentnumber (must be digit)")
        elif self.path == "sign":
            if "source" not in self.params or "documentid" not in self.params:
                raise Exception("Check source and/or document id parameter(s)")


class testClient:
    def __init__(self, uri) -> None:
        self.id = checkIdentity(uri)

    def get_path(self):
        return self.id.path

    def get_params(self):
        return self.id.params


client1 = testClient(
    "visma-identity://login?source=severa")
print(client1.get_path())
print(client1.get_params())
