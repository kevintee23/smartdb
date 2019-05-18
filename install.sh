#!/bin/bash

# Install script for smart Doorbell
# by de_man
# Run this script on /home/pi folder only
# 4/5/2019

#wget https://raw.githubusercontent.com/kevintee23/smartdb/master/install.sh

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
INFO  : Creating and Copying folders over...
-------------------------------------------------------------
"

cd ~
mkdir /home/pi/smartdb
echo '[+] /home/pi/smartdb folders have been created...'
mkdir /home/pi/smartdb/templates
mkdir /home/pi/smartdb/scripts
mkdir /home/pi/smartdb/static
cd ~
cd /home/pi/smartdb
wget -O gunicorn.service -q --show-progress https://raw.github.com/kevintee23/smartdb/master/gunicorn.service
wget -O hook.py -q --show-progress https://raw.github.com/kevintee23/smartdb/master/hook.py
wget -O takepicture.py -q --show-progress https://raw.github.com/kevintee23/smartdb/master/takepicture.py
wget -O README.md -q --show-progress https://raw.github.com/kevintee23/smartdb/master/README.md
wget -O config.py --show-progress https://raw.github.com/kevintee23/smartdb/master/config.py
cd ~
cd /home/pi/smartdb/templates
wget -O gallery.html -q --show-progress https://raw.github.com/kevintee23/smartdb/master/templates/gallery.html
wget -O picture.html -q --show-progress https://raw.github.com/kevintee23/smartdb/master/templates/picture.html
cd ~
cd /home/pi/smartdb/scripts
wget -O add_collection.py -q --show-progress https://raw.github.com/kevintee23/smartdb/master/scripts/add_collection.py
wget -O add_image.py -q --show-progress https://raw.github.com/kevintee23/smartdb/master/scripts/add_image.py
wget -O del_collections.py -q --show-progress https://raw.github.com/kevintee23/smartdb/master/scripts/del_collections.py
wget -O del_faces.py -q --show-progress https://raw.github.com/kevintee23/smartdb/master/scripts/del_faces.py
cd ~
cd /home/pi/smartdb/static
wget -O mysmartcave.jpg -q --show-progress https://raw.github.com/kevintee23/smartdb/master/static/mysmartcave.jpg

echo "
-------------------------------------------------------------
INFO  : Setting up permissions...
-------------------------------------------------------------
"
chmod +x /home/pi/smartdb/takepicture.py
sudo chown -R pi:pi /home/pi/smartdb/*
echo '[+] Permissions have been configured...'


echo "
-------------------------------------------------------------
INFO  : Cloning gunicorn service file to the appropriate folder
-------------------------------------------------------------
"
cd ~
cd /home/pi/smartdb
sudo chmod 755 gunicorn.service
cd
sudo cp /home/pi/smartdb/gunicorn.service /etc/systemd/system/


echo "
-------------------------------------------------------------
INFO  : Setting up daemon to run in the background...
-------------------------------------------------------------
"
cd /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn


echo "
-------------------------------------------------------------
INFO  : Leaning up old system files...
-------------------------------------------------------------
"
cd ~
rm -v install.sh
rm -v get-pip.py


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
