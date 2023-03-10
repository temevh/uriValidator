import re
from urllib.parse import urlparse


class checkIdentity:
    def __init__(self, uri):
        self.uri = uri
        self.path = None
        self.params = {}
        self.uriChecker()

    def uriChecker(self):
        # Using regex, make sure that the given URI starts with visma-identity://
        isValid = re.match("^visma-identity://.*", self.uri)
        if isValid:
            #print("URL IS VALID")
            parsed_uri = urlparse(self.uri)
            # Extract the path from the (validated) URI
            self.path = parsed_uri.netloc
            # print(self.path)
        else:
            raise Exception("CHECK URI SCHEME")

        # Make sure the URI path is recognized
        if self.path not in ['login', 'confirm', 'sign']:
            raise Exception("CHECK URI PATH")

        # Extract parameters from the URI
        parameters = re.search(r'\?(.*)', self.uri).group(1)
        # print(parameters)

        # Add the paremetes as key-value pairs to params dict
        for p in parameters.split("&"):
            key, value = p.split("=")
            if value == "":
                raise Exception("CHECK PARAMETERS")
            if key == "paymentnumber":  # make sure paymentnumber is stored as an integer
                value = int(value)
            self.params[key] = value

        # print(self.params)
        if self.path == "login":
            # Check that the "source parameter" exists AND that it is a string
            if "source" not in self.params or self.params["source"].isalpha() == False:
                raise Exception("CHECK SOURCE PARAMETER")

        elif self.path == "confirm":
            # Check that the source and paymentnumber parameters exist
            if "source" not in self.params or "paymentnumber" not in self.params:
                raise Exception(
                    "CHECK SOURCE AND/OR PAYMENTNUMBER PARAMETER(S)")

        elif self.path == "sign":
            if "source" not in self.params or "documentid" not in self.params:
                raise Exception("CHECK SOURCE AND/OR DOCUMENTID PARAMETER(S)")


class testClient:
    def __init__(self, uri) -> None:
        self.id = checkIdentity(uri)

    def get_params(self):
        return self.id.params

    def get_path(self):
        return self.id.path

    # An auxiliary function in case both parameters are needed with only one function call
    def returner(self):
        return self.id.params, self.id.path


testiUri = "visma-identity://sign?source=vismasign&documentid=105ab44"

client = testClient(testiUri)
print("path is", client.get_path())
print("parameters are", client.get_params())

# print(client.returner())
# (pls give job)
