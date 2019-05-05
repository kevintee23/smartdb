#!/bin/bash

# Install script for smart Doorbell
# by de_man
# 4/5/2019

cd

echo '[+] Installing and updating core dependencies...'
sudo apt-get update && sudo apt-get -y upgrade

echo '[+] Freeing up space. Removing Wolfram-Engine...'
sudo apt-get purge wolfram-engine

echo '[+] Installing python related dependencies...'
sudo apt-get install -yq python-picamera
sudo apt-get install -yq python3-picamera
sudo apt-get install -yq python-pip
sudo apt-get install -yq python3-pip

echo '[+] Installing gunicorn...'
sudo apt-get install gunicorn

echo '[+] Installing AWS CLI...'
sudo apt-get install awscli

echo '[+] Installing flask...'
sudo pip install flask

echo '[+] Installing required packages - boto3...'
sudo pip install boto3

echo '[+] Installing required packages - watchdog...'
sudo pip install watchdog

echo '[+] Installing required packages - simplejson...'
sudo pip install simplejson
rm -rf ~/.cache/pip

echo '[+] Cloning gunicorn service file to the appropriate folder'
sudo cp /home/pi/smartdb/gunicorn.service /etc/systemd/system/

echo '[+] Creating folder for captured pics...'
cd
mkdir /home/pi/smartdb/static

echo '[+] Setting up permissions...'
chmod +x /home/pi/smartdb/takepicture.py
sudo chown -R pi:pi /home/pi/smartdb/*

echo 'You will now need to manually configure AWS. To do this, type in aws configure...'

exit 0
