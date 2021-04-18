"""
In this file are stored the handle
functions to manage REST APIs.
Have fun
"""

import requests
import json
import random

SAVED_APIS = [(
        "TAYLOR", # code
        "https://api.taylor.rest", # endpoint
        {}, # arguments
        lambda t: "Taylor Swift says: " + json.loads(t)["quote"] # callback
    ), (
        "DADJOKE",
        "https://icanhazdadjoke.com/",
        {"headers": {"Accept": "application/json"}},
        lambda t: "A random dad joke: " + json.loads(t)["joke"]
    )
]

class API():
    def __init__(self, apis):
        self.__endpoints = {}
        for api in apis:
            self.addEndpoint(*api)

    def addEndpoint(self, code, ep, arguments, callback):
        self.__endpoints[code] = (ep, arguments, callback)

    def callEndpoint(self, code):
        ep, kwargs, callback = self.__endpoints[code]
        r = requests.get(ep, **kwargs)
        return callback(r.text)

    def callRandomEndpoint(self):
        code = random.choice(list(self.__endpoints.keys()))
        return self.callEndpoint(code)

    def __str__(self):
        return "\n".join("{} ({})".format(code, ep) for (code, (ep, _, _)) in self.__endpoints.items())
