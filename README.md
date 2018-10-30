# MITMProxy_PWNage

## Up & Running

### Installation

- git clone https://github.com/kr1tzb1tz/mitmproxy.git
- git clone https://github.com/kr1tzb1tz/MITMProxy_PWNage.git

### Development Setup

- ln -s ~/Playground/MITMProxy_PWNage/injector.py ~/Playground/mitmproxy/examples/addons/
- sudo apt-get install -y build-essential libbz2-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev curl vim firefox
- cd ~/Playground/ && curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
- echo 'export PATH="~/.pyenv/bin:$PATH" \
  eval "$(pyenv init -)" >> ~/.bashrc && exec $SHELL
- pyenv install 3.6.0 && pyenv global 3.6.0
- cd ~/Playground/mitmproxy/ && sudo ./dev.sh

### Firefox Setup

- Open preferences and search for proxy
  - Manually configure the proxy to localhost port 8080 for HTTP and HTTPS and press OK
- In the search bar go to "mitm.it" and download the cert for other.
  - Check both boxes and accept

### Running

- . venv/bin/activate
- mitmdump -s examples/addons/injector.py "google.com" "HTML" "TAGS" "h1|p" "Str8 Pwn3d"
- Go to google.com and wallah, Str8 Pwn3d!

---

## Custom Injection

- Run mitmdump -s injector.py [URL][mode] [SEARCH][regex] [REPLACEMENT]

  - [URL]

    - can be a FQDN or something as simple as "example" or "/stuff"
    - if left empty it will accept any domain
    - sys.argv[3]

  - [MODE]

    - Must be HTML or XML
    - sys.argv[4]

  - [SEARCH]

    - Must be TAGS or ANY
    - TAGS finds and replaces text in specific tags
    - ANY finds and replaces anything in the response
    - Literally ANYTHING!
    - sys.argv[5]

  - [REGEX]

    - For TAGS: the regex HAS to be for HTML or XML tags
      - ex) "h1" or "h1|p" or "h1|p|title"
    - For ANY the regex is for literally anything
      - ex) "dummy text" || "dummy|text"
    - sys.argv[6]

  - [REPLACEMENT]
    - whatever you want to replace the content with
      - ex) "Str8 Pwn3d"
    - sys.argv[7]

### Some Working Examples:

- mitmdump -s injector.py "example" "HTML" "ANY" "Example|example" "Meatball"
- mitmdump -s injector.py "example" "HTML" "TAGS" "h1|p" "Bacon is good"
