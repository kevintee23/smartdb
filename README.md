# smartdb
Smart Door Bell System

install.sh - will install all dependencies as well as set permissions

hook.py - a flask app that will run when a GET query is made to 0.0.0.0:5000 and execute takepicture.py

takepicture.py - snaps a photo and sends to aws rekognition to identify and post results to webcore

hoo.service - a guincorn daemon that will run the hook.py on the background
