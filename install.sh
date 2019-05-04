#!/bin/bash

# Install script for smart Doorbell
# by de_man
# 4/5/2019

cd

echo '[+] Installing and updating core dependencies...'
sudo apt-get update && sudo apt-get -y upgrade

echo '[+] Installing pip, gunicorn and AWS CLI...'
sudo apt-get install python-pip gunicorn python-requests awscli

echo '[+] Installing flask...'
sudo pip install flask

echo '[+] Installing required packages...'
sudo pip install boto3 watchdog simplejson ordereddict
rm -rf ~/.cache/pip

echo '[+] Cloning gunicorn service file to the appropriate folder'
sudo cp /home/pi/smartdb/gunicorn.service /etc/systemd/system/

echo '[+] Setting up permissions...'
cd smartdb
chmod +x takepicture.py

echo '[+] Creating folder for captured pics...'
cd
mkdir /home/pi/smartdb/static

echo '[+] Configure AWS...'
aws configure

echo 'May the force be with you...'
