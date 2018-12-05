# MITMProxy_PWNage

### Installation

- git clone https://github.com/kr1tzb1tz/mitmproxy.git
- git clone https://github.com/kr1tzb1tz/MITMProxy_PWNage.git

### MITMProxy + PWNage Plugin Setup

- (substitute ~/Playground/ with your clone path) 
- ln -s ~/Playground/MITMProxy_PWNage/injector.py ~/Playground/mitmproxy/examples/addons/
- sudo apt-get install -y build-essential libbz2-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev curl vim firefox python3.4-venv python3-pip
- cd ~/Playground/ && curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
- export PATH="~/.pyenv/bin:$PATH" eval "$(pyenv init -)" >> ~/.bashrc && exec $SHELL
- pyenv install 3.6.0 && pyenv global 3.6.0
- sudo pip3 install -Iv pytest-asyncio==0.9.0
	- Note: may need to install other python modules based on your setup
- cd ~/Playground/mitmproxy/ && sudo ./dev.sh

## Two ways to run

1. *The conservative way* for development, testing, etc.
	- Involves running MITMProxy locally with Firefox proxy settings manually set
1. *The fun way* for messing with friends, PWNing, etc.
	- Involves ARP poisoning and running MITMProxy to view and manipulate your targets' HTTP & HTTPS traffic

### The Conservative Way

- Setting up Firefox

#### Method 1 - Manual setup

- Open preferences and search for proxy
  - Manually configure the proxy to localhost port 8080 for HTTP and HTTPS and press OK
- In the search bar go to "mitm.it" and download the cert for other.
  - Check both boxes and accept

#### Method 2 - Run the install.sh script
	- ./install.sh
	- This installs the certificate and an adequate firefox profile with proxying to port 8080 enabled. 

#### Running

- . venv/bin/activate
- mitmdump -s examples/addons/injector.py "google.com" "TAGS" "h1|p" "Str8 Pwn3d"
- Go to google.com and wallah, Str8 Pwn3d!

### The Fun Way

- Setting up Ettercap

---

## Custom Injection

- Run mitmdump -s injector.py [URL] [SEARCH] [regex] [REPLACEMENT]

  - [URL]

    - can be a FQDN or something as simple as "example" or "/stuff"
    - if left empty it will accept any domain
    - sys.argv[2]

  - [SEARCH]

    - Must be TAGS or ANY
    - TAGS finds and replaces text in specific tags
    - ANY finds and replaces anything in the response
    - Literally ANYTHING!
    - sys.argv[4]

  - [REGEX]

    - For TAGS: the regex HAS to be for HTML or XML tags
      - ex) "h1" or "h1|p" or "h1|p|title"
    - For ANY the regex is for literally anything
      - ex) "dummy text" || "dummy|text"
    - sys.argv[5]

  - [REPLACEMENT]
    - whatever you want to replace the content with
      - ex) "Str8 Pwn3d"
    - sys.argv[6]

### Some Working Examples:

- mitmdump -s injector.py "example" "ANY" "Example|example" "Meatball"
- mitmdump -s injector.py "example" "TAGS" "h1|p" "Bacon is good"
