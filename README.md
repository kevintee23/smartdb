# smartdb
Smart Door Bell System

This script works on a Raspberry Pi with a Raspberry Camera module. Tailored to work with SmartThings and webCoRE. Basically when a motion is detected or a button is pressed, webCoRE will then initiate a GET request to the Raspberry Pi. When the response is received is received on the RPi, it will take a picture within 1 second. The picture is then sent over to AWS Rekognition for facial recognition.

install.sh - will install all dependencies as well as set permissions

hook.py - a flask app that will run when a GET query is made to 0.0.0.0:5000 and execute takepicture.py

takepicture.py - snaps a photo and sends to aws rekognition to identify and post results to webcore

hoo.service - a guincorn daemon that will run the hook.py on the background
