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

    CACHE_MAX = 10

    def __init__(self, apis):
        self.__endpoints = {}
        self.__cache = []
        for api in apis:
            self.addEndpoint(*api)

    def addEndpoint(self, code, ep, arguments, callback):
        self.__endpoints[code] = (ep, arguments, callback)

    def populateCache(self):
        size = len(self.__cache)
        temp = []
        for _ in range(API.CACHE_MAX - size):
            temp.append(self.callRandomEndpoint())
        self.__cache = temp

    def checkCache(self):
        if len(self.__cache) > 0:
            return self.__cache.pop()
        return None

    def callRandomEndpoint(self):
        res = self.checkCache()
        if res is not None: return res
        code = random.choice(list(self.__endpoints.keys()))
        while True:
            res = self.callEndpoint(code)
            if res is None: continue
            return res

    def callEndpoint(self, code):
        ep, kwargs, callback = self.__endpoints[code]
        r = requests.get(ep, **kwargs)
        if r.status_code == 200:
            try: return callback(r.text)
            except KeyError: traceback.print_exc()
        return None

    def __str__(self):
        return "\n".join("{} ({})".format(code, ep) for (code, (ep, _, _)) in self.__endpoints.items())

if __name__ == "__main__":
    api = API(SAVED_APIS)
    api.populateCache()

    print("Calling 10 random endpoints")
    for _ in range(10):
        print(api.callRandomEndpoint())

    print("Calling all available APIs")
    for code, *_ in SAVED_APIS:
        print("=> " + code)
        print(api.callEndpoint(code))
