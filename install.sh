#!/bin/bash

# Install script for smart Doorbell
# by de_man
# 4/5/2019

cd

echo "
-------------------------------------------------------------
INFO  : Installing and updating core dependencies...
-------------------------------------------------------------
"
sudo apt-get update && sudo apt-get -y upgrade

echo "
-------------------------------------------------------------
INFO  : $STATUS Freeing up space. Removing Wolfram-Engine...
-------------------------------------------------------------
"
sudo apt-get purge wolfram-engine


echo "
-------------------------------------------------------------
INFO  : $STATUS Installing pip from pypa.io...
-------------------------------------------------------------
"
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py

echo "
---------------------------------------------------------------------
INFO  : $STATUS Installing gunicorn, cause who doesn't love unicorns!
---------------------------------------------------------------------
"
sudo apt-get install -y gunicorn

echo "
-------------------------------------------------------------
INFO  : $STATUS Installing AWS CLI...
-------------------------------------------------------------
"
sudo apt-get install -y awscli

echo "
-------------------------------------------------------------
INFO  : $STATUS Installing Flask webserver...
-------------------------------------------------------------
"
sudo python -m pip install flask

echo "
-------------------------------------------------------------
INFO  : $STATUS Installing boto3, the AWS rekognition client...
-------------------------------------------------------------
"
sudo python -m pip install boto3

echo "
-------------------------------------------------------------
INFO  : $STATUS Installing requests...
-------------------------------------------------------------
"
sudo python -m pip install requests

echo "
-------------------------------------------------------------
INFO  : $STATUS Installing simplejson...
-------------------------------------------------------------
"
sudo python -m pip install simplejson
rm -rf ~/.cache/pip

echo "
-------------------------------------------------------------
INFO  : Cloning gunicorn service filr to the appropriate folder
-------------------------------------------------------------
"
sudo cp /home/pi/smartdb/gunicorn.service /etc/systemd/system/

echo "
-------------------------------------------------------------
INFO  : Creating a folder for all your pictures...
-------------------------------------------------------------
"
cd
mkdir /home/pi/smartdb/static

echo "
-------------------------------------------------------------
INFO  : Setting up permissions...
-------------------------------------------------------------
"
chmod +x /home/pi/smartdb/takepicture.py
sudo chown -R pi:pi /home/pi/smartdb/*

echo "
-------------------------------------------------------------
INFO  : Setting up daemon to run in the background...
-------------------------------------------------------------
"
cd
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

echo "
-------------------------------------------------------------
INFO  : $STATUS Completed!! Just a few more things...
-------------------------------------------------------------
A few things before you start.

1 - setup your AWS settings by typing in 'aws configure' on your terminal screen.

2 - Activate your raspberry pi camera by typing on terminal:-
    - sudo raspi-config
    - go to 'Interfacing Options'
    - Select P1 Camera
    - Select Yes to enable it
    - system will reboot
    
3 - To check if the service is running in the background, so that the service will keep on running when you exit terminal,
    type in 'systemctl status gunicorn'. You should see that some messages that say 'Active: active (running). If it is not
    for some reason, run the following command:-
    - sudo systemctl daemon-reload
    - sudo systemctl start gunicorn
    - sudo systemctl enable gunicorn
"

exit 0
