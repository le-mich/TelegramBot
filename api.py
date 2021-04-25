"""
In this file are stored the handle
functions to manage REST APIs.
Have fun
"""

import requests
import json
import random
import traceback

# This APIs are automatically added to the pool, to add one
# create a new tuple at the end of this list with
#   - code: id of the REST API, just pick an original one
#   - endpoint: the REST API endpoint
#   - paramters: eventual parameters
#   - callback: the function called on the response's body
SAVED_APIS = [(
        "TAYLOR", # code
        "https://api.taylor.rest", # endpoint
        {}, # arguments
        lambda t: "Taylor Swift says: " + json.loads(t)["quote"] # callback
    ), (
        "DADJOKE",
        "https://icanhazdadjoke.com/",
        {"headers": {"Accept": "application/json"}},
        lambda t: json.loads(t)["joke"]
    ), (
        "CATFACTS",
        "http://catfact.ninja/fact",
        {},
        lambda t: "Cat fact: " + json.loads(t)["fact"]
    ), (
        "DOGFACTS",
        "https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1",
        {},
        lambda t: "Dog fact: " + json.loads(t)[0]["fact"]
    ), (
        "JOKE",
        "https://v2.jokeapi.dev/joke/Any",
        {},
        lambda t: "{}\n{}".format(json.loads(t)["setup"], json.loads(t)["delivery"])
    ), (
        "JOKE2",
        "https://official-joke-api.appspot.com/random_joke",
        {},
        lambda t: "{}\n{}".format(json.loads(t)["setup"], json.loads(t)["punchline"])
    ), (
        "JOKE3",
        "https://api.jokes.one/jod",
        {"headers": {"Accept": "application/json"}},
        lambda t: "{}\n{}".format(json.loads(t)["contents"]["jokes"][0]["joke"]["title"], json.loads(t)["contents"]["jokes"][0]["joke"]["text"])
    ), (
        "TRUMP",
        "https://api.tronalddump.io/random/quote",
        {},
        lambda t: "Donald Trump once said: " + json.loads(t)["value"]
    ), (
        "INSULT",
        "https://evilinsult.com/generate_insult.php?lang=en&type=json",
        {},
        lambda t: json.loads(t)["insult"]
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
        if r.status_code == 200:
            try: return callback(r.text)
            except KeyError: traceback.print_exc()
        return None

    def callRandomEndpoint(self):
        code = random.choice(list(self.__endpoints.keys()))
        while (res := self.callEndpoint(code)) is None:
            continue
        return res

    def __str__(self):
        return "\n".join("{} ({})".format(code, ep) for (code, (ep, _, _)) in self.__endpoints.items())

if __name__ == "__main__":
    # Test all saved APIs

    api = API(SAVED_APIS)

    for code, *_ in SAVED_APIS:
        print("=> " + code)
        print(api.callEndpoint(code))
