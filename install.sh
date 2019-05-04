#!/bin/bash

# Install script for smart Doorbell
# by de_man
# 4/5/2019

cd

echo '[+] Installing and updating core dependencies...'
sudo apt-get update && sudo apt-get -y upgrade

echo '[+] Installing pip, gunicorn and AWS CLI...'
sudo apt-get install python-pip gunicorn awscli

echo '[+] Installing requests...'
python -m pip install --user requests

echo '[+] Installing flask...'
sudo pip install flask

echo '[+] Installing required packages...'
sudo pip install boto3 watchdog simplejson
rm -rf ~/.cache/pip

echo '[+] Cloning gunicorn service file to the appropriate folder'
sudo cp /home/pi/smartdb/gunicorn.service /etc/systemd/system/

echo '[+] Creating folder for captured pics...'
cd
mkdir /home/pi/smartdb/static

echo '[+] Setting up permissions...'
cd smartdb
chmod +x takepicture.py
sudo chown -R pi:pi /home/pi/smartdb/*

echo 'You will now need to manually configure AWS. To do this, type in aws configure...'
