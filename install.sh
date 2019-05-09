#!/bin/bash

# Install script for smart Doorbell
# by de_man
# Run this script on /home/pi folder only
# 4/5/2019

#wget https://raw.githubusercontent.com/kevintee23/smartdb/master/install.sh

#COLORS
# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan

#Informational only, getting your IP Address
ip=$(hostname -I | cut -f1 --delimiter=' ')
echo "Your Raspberry Pi IP Address is $ip"

cd

echo "$Cyan
-------------------------------------------------------------
INFO  : Installing and updating core dependencies...
-------------------------------------------------------------
$Color_Off"
sudo apt-get update && sudo apt-get -y upgrade

echo "$Cyan
-------------------------------------------------------------
INFO  : $STATUS Freeing up space. Removing Wolfram-Engine...
-------------------------------------------------------------
$Color_Off"
wolfram="y"
nowolfram="y"
echo "$Green Would you like to free up some space by removing the Wolfram-Engine? $Color_Off"
read "Perform space saver routine? Enter y for yes or n for no (default= $wolfram): " nowolfram
[ -n "$nowolfram" ] && wolfram=$nowolfram

if [ "$wolfram" = "y" ];
then
    echo "$Cyan Removing Wolfram-Engine... $Color_Off"
    sudo apt-get purge wolfram-engine
else
    echo "$Cyan Skipping this step and moving on... $Color_Off"
    
fi

echo "$Cyan
-------------------------------------------------------------
INFO  : $STATUS Installing pip from pypa.io...
-------------------------------------------------------------
$Color_Off"
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py

echo "$Cyan
---------------------------------------------------------------------
INFO  : $STATUS Installing gunicorn, cause who doesn't love unicorns!
---------------------------------------------------------------------
$Color_Off"
sudo apt-get install -y gunicorn

echo "$Cyan
-------------------------------------------------------------
INFO  : $STATUS Installing AWS CLI...
-------------------------------------------------------------
$Color_Off"
sudo apt-get install -y awscli

echo "$Cyan
-------------------------------------------------------------
INFO  : $STATUS Installing Flask webserver...
-------------------------------------------------------------
$Color_Off"
sudo python -m pip install flask

echo "$Cyan
-------------------------------------------------------------
INFO  : $STATUS Installing boto3, the AWS rekognition client...
-------------------------------------------------------------
$Color_Off"
sudo python -m pip install boto3

echo "$Cyan
-------------------------------------------------------------
INFO  : $STATUS Installing requests...
-------------------------------------------------------------
$Color_Off"
sudo python -m pip install requests

echo "$Cyan
-------------------------------------------------------------
INFO  : $STATUS Installing simplejson...
-------------------------------------------------------------
$Color_Off"
sudo python -m pip install simplejson
rm -rf ~/.cache/pip

echo "$Cyan
-------------------------------------------------------------
INFO  : Creating and Copying folders over...
-------------------------------------------------------------
$Color_Off"

cd ~
mkdir /home/pi/smartdb
echo '$Cyan /home/pi/smartdb created... $Color_Off'
mkdir /home/pi/smartdb/templates
mkdir /home/pi/smartdb/scripts
mkdir /home/pi/smartdb/static
cd ~
cd /home/pi/smartdb
wget -O gunicorn.service -q --show-progress https://raw.github.com/kevintee23/smartdb/master/gunicorn.service
wget -O hook.py -q --show-progress https://raw.github.com/kevintee23/smartdb/master/hook.py
wget -O takepicture.py -q --show-progress https://raw.github.com/kevintee23/smartdb/master/takepicture.py
wget -O README.md -q --show-progress https://raw.github.com/kevintee23/smartdb/master/README.md
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

echo "$Cyan
-------------------------------------------------------------
INFO  : Setting up permissions...
-------------------------------------------------------------
$Color_Off"
chmod +x /home/pi/smartdb/takepicture.py
sudo chown -R pi:pi /home/pi/smartdb/*

echo "$Cyan
-------------------------------------------------------------
INFO  : Cloning gunicorn service file to the appropriate folder
-------------------------------------------------------------
$Color_Off"
cd home/pi/smartdb
sudo chmod 755 gunicorn.service
cd
sudo cp /home/pi/smartdb/gunicorn.service /etc/systemd/system/


echo "$Cyan
-------------------------------------------------------------
INFO  : Setting up daemon to run in the background...
-------------------------------------------------------------
$Color_Off"
cd /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

fi

echo "$Cyan
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
$Color_Off"

exit 0
