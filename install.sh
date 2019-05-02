#!/bin/bash

# Install script for cameraTest
# by de_man
# 23/4/2019

cd

echo '[+] Installing and updating core dependencies...'
sudo apt-get update && sudo apt-get -y upgrade

echo '[+] Installing pip, gunicorn and AWS CLI...'
sudo apt-get install python-pip gunicorn awscli

echo '[+] Installing flask...'
sudo pip install flask

echo '[+] Installing required packages...'
sudo pip install boto3 watchdog simplejson PiCamera
rm -rf ~/.cache/pip

echo '[+] Cloning gunicorn service file to the appropriate folder'
sudo cp /home/pi/cameraTest/cameraTest.service /etc/systemd/system/

echo '[+] Setting up permissions...'
cd cameratest
chmod +x takepicture.sh

echo '[+] Creating folder for captured pics...'
cd
mkdir /home/pi/smartdb/static

echo '[+] Configure AWS...'
aws configure

echo 'May the force be with you...'
