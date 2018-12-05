from bs4 import BeautifulSoup
from mitmproxy import http
import re

URL         =   "google"
SEARCH      =   "ANY"
REGEX       =   "Lucky"
INJECT      =   "Hack3d"


class Injector:

    # Checks # of arguments and yells at you if not correct
    def load(self, loader):
        print("\n---> Addon loaded!\n")

    # Method for manipulating stuff
    def response(self, flow: http.HTTPFlow) -> None:

        # Checks the URL
        if URL in flow.request.pretty_host:
            soup = BeautifulSoup(flow.response.content, "html.parser")

           # Checks the SEARCH
            if SEARCH == "TAGS":
                # Checks content
                if soup is not None:
                    # Regex creation
                    regex = re.compile(REGEX)
                    # Search the soup using regex and replace stuff
                    for tag in soup.find_all(regex):
                        print("-> Replaced %s" % (tag))
                        tag.string = INJECT
                        print("-> with %s\n" % (tag))
                else:
                    print("-> No soup for you!")

                # Assign the actual response body the code we  messed with
                flow.response.content = str(soup).encode("utf8")

            # Checks the SEARCH
            elif SEARCH == "ANY":
                # Checks content
                if soup is not None:
                    # Regex creation
                    regex = re.compile(REGEX)
                    # Create string soup!
                    stringSoup = str(soup)
                    # Create a list of anything that matches the regex
                    results = re.findall(regex, stringSoup)
                    # Replace the results with our REPLACEMENT
                    for result in results:
                        stringSoup = stringSoup.replace(
                            result, INJECT)
                        print("-> Replaced %s" % (result))
                        print("-> with %s\n" % (INJECT))

                    # Assign the response body our stuff
                    flow.response.content = stringSoup.encode("utf8")

                else:
                    print("-> No soup for you!")
            else:
                print("Mode has to be TAGS or ANY")


# MITMProxy add-ons
addons = [
    Injector()
]
