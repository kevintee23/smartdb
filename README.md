# smartdb
Smart Door Bell System (Not Completed)

This script works on a Raspberry Pi with a Raspberry Camera module. Tailored to work with SmartThings and webCoRE. Basically when a motion is detected or a button is pressed, webCoRE will then initiate a GET request to the Raspberry Pi. When the response is received is received on the RPi, it will take a picture within 1 second. The picture is then sent over to AWS Rekognition for facial recognition. The response from rekognition is then passed over to webCoRE for more advanced automations.

On your raspberry pi terminal enter - <code>wget https://raw.githubusercontent.com/kevintee23/smartdb/master/install.sh</code>



Once completed, type in the following- <code>bash ./install.sh</code>





Required to get an AWS Rekognition account and obtain Access Key ID and Secret Access Key. Once that has been obtain, when user run 'aws configure' they will need to enter those information. As for the region setting, it should also be the same when setting up the AWS Rekognition account (tested and working on us-west-2).

Once that is setup, you will need to create a collection. To create a collection:-

<li><code>cd</code></li>
<li><code>cd /smartdb/script</code></li>
<li><code>python add_collection.py -n 'collectionName'</code></li>
#enter the name of the collection like 'home' or 'family' or 'peopleiknow'. You can create as many, but only 1 collection will work for this automation.

You will then need to rekognition to know who is who. Around 3-5 images per person would be good.
```
<li><code>cd</code></li>
<li><code>cd /smartdb/faces</code></li>
<li><code>python /home/pi/smartdb/scripts/add_faces.py -i 'imagename.jpg' -c 'collectionName' -l 'name'</code></li>
```

<b>Files</b>

install.sh - will install all dependencies as well as set permissions

hook.py - a flask app that will run when a GET query is made to 0.0.0.0:5000 and execute takepicture.py

takepicture.py - snaps a photo and sends to aws rekognition to identify and post results to webcore

gunicorn.service - a guincorn daemon that will run the hook.py on the background


<b>About Saved Snapshots</b>

The pictures that the camera captures will be appropriately named based on the time of capture. To ensure that it makes sense and is local to you, you will need to update your time on your RPI. To do this:-

<li><code>sudo raspi-config</code><li>
  
  From there, go to the Localization Options and select your timezone. Once that is done, the captured images will let you know when the picture was taken.

```
2018-03-31T18:27:09.508Z a90824f40764eb5df1fccc4f5cb95dd3 reconnectionManagement(): reconnecting
```
