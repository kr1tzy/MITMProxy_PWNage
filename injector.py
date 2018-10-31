from bs4 import BeautifulSoup
from mitmproxy import http
import sys
import re

class Injector:

    # Checks # of arguments and yells at you if not correct
    def load(self, loader):
        if len(sys.argv) == 7:
            print("\n---> Addon loaded!\n")
        else:
            print("\n---> Wrong number of args for addon.")
            print("---> mitmdump -s addon.py"
                  + "<URL> <SEARCH> <REGEX> <REPLACEMENT>")
            print("---> Running mitmproxy w/o addon\n")

    # Method for manipulating stuff
    def response(self, flow: http.HTTPFlow) -> None:

        # Checks # of args
        if len(sys.argv) == 7:

            # Checks the URL
            if sys.argv[3] in flow.request.pretty_host:

                # Checks the SEARCH
                if sys.argv[4] == "TAGS":
                    # Checks content
                    if soup is not None:
                        # Regex creation
                        regex = re.compile(sys.argv[5])
                        # Search the soup using regex and replace stuff
                        for tag in soup.find_all(regex):
                            print("-> Replaced %s" % (tag))
                            tag.string = sys.argv[6]
                            print("-> with %s\n" % (tag))
                    else:
                        print("-> No soup for you!")

                    # Assign the actual response body the code we  messed with
                    flow.response.content = str(soup).encode("utf8")

                # Checks the SEARCH
                elif sys.argv[5] == "ANY":
                    # Checks content
                    if soup is not None:
                        # Regex creation
                        regex = re.compile(sys.argv[5])
                        # Create string soup!
                        stringSoup = str(soup)
                        # Create a list of anything that matches the regex
                        results = re.findall(regex, stringSoup)
                        # Replace the results with our REPLACEMENT
                        for result in results:
                            stringSoup = stringSoup.replace(
                                result, sys.argv[6])
                            print("-> Replaced %s" % (result))
                            print("-> with %s\n" % (sys.argv[6]))

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
