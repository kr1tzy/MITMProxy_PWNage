from bs4 import BeautifulSoup
from mitmproxy import http
import sys
import re


#   To use
#   -----
#
#   * Enter the virtual env from the mitmproxy home directory
#
#       -> . venv/bin/activate
#
#   * Run mitm[dump|web|proxy] \
#         > -s addon.py <URL> <MODE> <SEARCH> <REGEX> <REPLACEMENT>
#
#       -> <URL>
#           -> can be a FQDN or something as simple as "example" or "/stuff"
#           -> if left empty it will accept any domain
#           -> sys.argv[3]
#
#       -> <MODE> HTML || XML
#           -> sys.argv[4]
#
#       -> <SEARCH> TAGS || ANY
#           -> TAGS finds and replaces text in specific tags
#           -> ANY finds and replaces anything in the response
#               -> Literally ANYTHING!
#           -> sys.argv[5]
#
#       -> <REGEX>
#           -> TAGS: the regex HAS to be for HTML or XML tags
#               -> ex) "h1"  or "h1|p" or "h1|p|title"
#           -> For ANY the regex is for literally anything
#               -> ex) "dummy text" || "Example|domain"
#           -> sys.argv[6]
#
#       -> <REPLACEMENT> whatever you want to replace the content with
#           -> sys.argv[7]
#
#   Working Examples:
#
#   mitmdump -s addon.py "example" "HTML" "ANY" "Example|example" "Meatball"
#   mitmdump -s addon.py "example" "HTML" "TAGS" "h1|p" "Bacon is good"
#
class Injector:

    # Checks # of arguments and yells at you if not correct
    def load(self, loader):
        if len(sys.argv) == 8:
            print("\n---> Addon loaded!\n")
        else:
            print("\n---> Wrong number of args for addon.")
            print("---> mitmdump -s addon.py"
                  + "<URL> <MODE> <SEARCH> <REGEX> <REPLACEMENT>")
            print("---> Running mitmproxy w/o addon\n")

    # Method for manipulating stuff
    def response(self, flow: http.HTTPFlow) -> None:

        # Checks # of args
        if len(sys.argv) == 8:

            # Checks the URL
            if sys.argv[3] in flow.request.pretty_host:

                # Checks the MODE
                if sys.argv[4] == "HTML":
                    soup = BeautifulSoup(
                        flow.response.content, "html.parser")
                elif sys.argv[4] == "XML":
                    soup = BeautifulSoup(flow.response.content, "xml")
                else:
                    print("---> MODE was inputted wrong. HTML or XML")

                # Checks the SEARCH
                if sys.argv[5] == "TAGS":
                    # Checks content
                    if soup is not None:
                        # Regex creation
                        regex = re.compile(sys.argv[6])
                        # Search the soup using regex and replace stuff
                        for tag in soup.find_all(regex):
                            print("-> Replaced %s" % (tag))
                            tag.string = sys.argv[7]
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
                        regex = re.compile(sys.argv[6])
                        # Create string soup!
                        stringSoup = str(soup)
                        # Create a list of anything that matches the regex
                        results = re.findall(regex, stringSoup)
                        # Replace the results with our REPLACEMENT
                        for result in results:
                            stringSoup = stringSoup.replace(
                                result, sys.argv[7])
                            print("-> Replaced %s" % (result))
                            print("-> with %s\n" % (sys.argv[7]))

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
