# MITMProxy_PWNage/firefox

## About

- The **./install.sh** script installs a certificate and updates the Firefox proxy settings to proxy to port 8080. Meant to be ran on a target's machine.
- In order to avoid getting the security exception, one can run the **install.sh** script in the Victim VM (or locally) to install the MITMProxy cert. If this is not a previously accepted certificate the exception will come up each time prompting the user to avoid going to the site.
	- *Note:* in order to run the **./install.sh** script on the Victim VM successfully the IP address should be changed inside the script to the Attack VM's.

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
