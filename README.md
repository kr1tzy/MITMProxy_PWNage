# MITMProxy_PWNage

## About
- MITMProxy_PWNage is a final project for the Network Security (CSE 5473) class at The Ohio State University. It demonstrates the power and flexiblity of MITMProxy by exhibiting our _injector.py_ plugin alongside an ARP poisoning attack via Ettercap. The _injector.py_ plugin dynamically finds and replaces text in a web response by parsing the HTML tags or following a regular expression. It can be utilized for both HTTP & HTTPS traffic. 
- Below we indicate two ways to play with the project: **The Fun Way** and **The Conservative Way**. **The Fun Way** is intended to be set up in a controlled virtualized network that will not touch a public domain. Furthermore, **The Conservative Way** is contained within a single virtual machine that will not touch a public domain. It can be used for testing, development, etc. 
- We assume users will exercise caution, descretion, common sense, and judgement while using these tools and do not take responsibility for their actions.

1. **The Fun Way** for messing with friends, PWNing, etc.
	- Involves ARP poisoning and running MITMProxy to view and manipulate your targets' HTTP & HTTPS traffic.

2. **The Conservative Way** for development, testing, etc.
	- Involves running MITMProxy locally with Firefox proxy settings manually set in Firefox. Tested on Ubuntu 18.04.

## The Fun Way

- Virtual Network Setup
- Setting up Ettercap
- MITMProxy + Plugin
- IP Forwarding
- Run the plugin

### Virtual Network Setup
-	Inside of whatever virtualization software you use set up a shared NAT network. As an example, with VirtualBox go to VirtualBox->Preferences->Network and add an NAT Network. The network CIDR can be whatever you want, but for our demonstration we will use 10.0.2.0/24. Give it a name (e.g., NATNetw0rk), and check "Enable Network".
- Create two virtual machines, we used Ubuntu 18.04 for our "Attack" machine and Lubuntu 14.04 for our "Victim" machine. You can use whatever flavor of Linux you want but be mindful about setup differences. From here on out these machines will be denoted "Attack VM" and "Victim VM", respectively.
- Configure the network settings of each VM in VirtualBox, make sure their network cards are using the NAT network you created, in our case NATNetw0rk.
- After the VMs are created, statically assign IPs to each machine by configuring the interfaces in a similar (or identical) fashion.

-  **Attack VM** /etc/network/interfaces
```
auto lo
iface lo inet loopback 

auto enp0s3
 iface enp0s3 inet static
   address 10.0.2.3
   netmask 255.255.255.0
   gateway 10.0.2.1
   dns-nameservers 8.8.8.8
```

-  **Victim VM** /etc/network/interfaces
```
auto lo
iface lo inet loopback 

auto eth0
 iface eth0 inet static
   address 10.0.2.5
   netmask 255.255.255.0
   gateway 10.0.2.1
   dns-nameservers 8.8.8.8
```

- Restart the networking service of each VM.

```
sudo systemctl restart networking.service
```

- Make sure you can ping each other. For example, from the Attack VM ping 10.0.2.5, and from the Victim VM ping 10.0.2.3. You should be getting responses from both machines. Now we can set up Ettercap on the Attack VM.

### Ettercap Setup (on Attack VM)

- sudo sysctl -w net.ipv4.ip_forward=1
- sudo apt-get install ettercap-graphical
- sudo ettercap -G
- Under "Sniff" select "Unified Sniffing" and select the interface that was configured for the Attack VM - in our case it is enp0s3. Select "Ok".
- Go into "Hosts" and select "Hosts list"
	- Click "Hosts" again and select "Scan for hosts"
	- Add 10.0.2.1 (default gateway) to "Target 1"
	- Add 10.0.2.5 (Victim VM) to "Target 2"
- Now click on "Mitm" and then "ARP poisoning..."
	-	Check the "Sniff remote connections." box and click "Ok"
- To verify we're getting traffic open a terminal and run sudo tcpdump. In the Victim VM open Firefox and go to google.com and come back to the tcpdump terminal screen and watch the traffic flow. Facebook won't populate on the Victim VM because we're not forwarding anything yet; however, we proved we're getting the traffic from the Victim VM so we can do IP forwarding and setup MITMProxy.

### IP Forwarding

- Run the following in the Attack VM
	- Make sure you have the right interface

```
sudo iptables -t nat -A PREROUTING -i enp0s3 -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -A PREROUTING -i enp0s3 -p tcp --dport 443 -j REDIRECT --to-port 8080
```

- To confirm run sudo iptables -t nat -L

### MITMProxy + _injector.py_ Plugin

- git clone https://github.com/kr1tzb1tz/mitmproxy.git
- git clone https://github.com/kr1tzb1tz/MITMProxy_PWNage.git
- Substitute ~/Playground/ with your specific path
- ln -s ~/Playground/MITMProxy_PWNage/injector.py ~/Playground/mitmproxy/examples/addons/
- sudo apt-get install -y build-essential libbz2-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev curl python3-venv
- cd ~/Playground/ && curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
- echo eval "$(pyenv init -)" >> ~/.bashrc && exec $SHELL
- pyenv install 3.6.0 && pyenv global 3.6.0
- cd ~/Playground/mitmproxy/ && sudo ./dev.sh
- _Note_: on some systems you may need to install other python modules, just follow along with any error messages and download what it yells at you about.

### Running

- . venv/bin/activate
- View the _injector.py_ instructions below or view the source code to understand what you can do but the following example works.
	- mitmdump -s examples/addons/injector.py "example.com" "TAGS" "h1|p" "Str8 Pwn3d!"
- Go to https://example.com in the Victim VM & wallah, Str8 Pwn3d!

## The Conservative Way

- Set up MITMProxy + Plugin
- Set up Firefox to proxy our MITMProxy instance
- Run the plugin

### MITMProxy + _injector.py_ Plugin

- git clone https://github.com/kr1tzb1tz/mitmproxy.git
- git clone https://github.com/kr1tzb1tz/MITMProxy_PWNage.git
- Substitute ~/Playground/ with your specific path
- ln -s ~/Playground/MITMProxy_PWNage/injector.py ~/Playground/mitmproxy/examples/addons/
- sudo apt-get install -y build-essential libbz2-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev curl python3-venv
- cd ~/Playground/ && curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
- echo eval "$(pyenv init -)" >> ~/.bashrc && exec $SHELL
- pyenv install 3.6.0 && pyenv global 3.6.0
- cd ~/Playground/mitmproxy/ && sudo ./dev.sh
- _Note_: on some systems you may need to install other python modules, just follow along with any error messages and download what it yells at you about.

### Setting up Firefox

#### Method 1 - Manual setup

- Open preferences of Firefox and search for proxy
  - Manually configure the proxy to localhost port 8080 for HTTP and HTTPS and press OK
- In the search bar go to "mitm.it" and download the cert.
  - Check both boxes and accept
- Run the plugin

#### Method 2 - Run the install.sh script
- cd firefox && ./install.sh
- This installs the MITMProxy certificate and an adequate firefox profile with proxying to port 8080.
- Run the plugin

### Running

- . venv/bin/activate
- View the _injector.py_ instructions below or view the source code to understand what you can do but the following example works.
- mitmdump -s examples/addons/injector.py "example.com" "TAGS" "h1|p" "Str8 Pwn3d!"
- Go to https://example.com and wallah, Str8 Pwn3d!


## Injector.py

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

### Working Examples:

- mitmdump -s injector.py "example.com" "ANY" "Example" "Meatball"
- mitmdump -s injector.py "example.com" "TAGS" "h1|p" "Bacon is lyfe"


--- 


### Our Team

- Noah Kritz - @kr1tzb1tz
- Laura Mobley - @lauramobley
- Sam Wolfe - @wolfe766
- John Sparks - @Sparks2017

### Acknowledgements

- [MITMProxy](https://github.com/mitmproxy/mitmproxy) 
- [Ettercap](https://github.com/Ettercap/ettercap)
