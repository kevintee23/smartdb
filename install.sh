#!/bin/bash

# Install script for smart Doorbell
# by de_man
# Run this script on /home/pi folder only
# 4/5/2019

#wgethttps://raw.githubusercontent.com/kevintee23/smartdb/master/install.sh

#Informational only, getting your IP Address
ip=$(hostname -I | cut -f1 --delimiter=' ')
echo "Your Raspberry Pi IP Address is $ip"

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
wolfram="y"
nowolfram="y"
echo "Would you like to free up some space by removing the Wolfram-Engine?"
read "Perform space saver routine? Enter y for yes or n for no (default= $wolfram): " nowolfram
[ -n "$nowolfram" ] && wolfram=$nowolfram

if [ "$wolfram" = "y" ];
then
    echo "Removing Wolfram-Engine..."
    sudo apt-get purge wolfram-engine
else
    echo "Skipping this step and moving on..."
    
fi

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
INFO  : Cloning gunicorn service file to the appropriate folder
-------------------------------------------------------------
"
cd home/pi/smartdb
sudo chmod 755 gunicorn.service
cd
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
cd /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

fi

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
    type in 'ps -ef | grep gunicorn'. You should see that some messages that say 
    '/usr/bin/python /usr/bin/gunicorn -b 0.0.0.0:5000'. If it is not for some reason, run the following command:-
    - sudo systemctl daemon-reload
    - sudo systemctl start gunicorn
    - sudo systemctl enable gunicorn
"

exit 0
