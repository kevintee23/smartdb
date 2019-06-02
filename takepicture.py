#!/usr/bin/env python

import boto3 as b3
import StringIO
from time import gmtime, strftime
import requests
from collections import OrderedDict
import json
import os
import socket
import time
import subprocess
from datetime import datetime
from ConfigParser import ConfigParser

#File Settings
diskSpaceToReserve = 40 * 1024 * 1024 #Keep 40mb free on disk
config = ConfigParser()

config.read('config1.ini')
 
def get_client():
    return b3.client('rekognition')

#Takes a picture and names it    
def take_picture(diskSpaceToReserve):
	keepDiskSpaceFree(diskSpaceToReserve)
	time = datetime.now()
	quality = config.get('Camera Settings', 'picQuality')
	vflip = config.get('Camera Settings', 'vflip')
	hflip = config.get('Camera Settings', 'hflip')
	filename = "/home/pi/smartdb/static/capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)

	print '[+] A photo is being taken now...'

	subprocess.call("raspistill -o %s --timeout 1 --nopreview --exposure sports -q %s -a 1036 -ae +75+75 %s %s" % (filename, quality, vflip, hflip), shell=True)
	print '[+] Your image was saved to %s...' % filename
	return filename

#Keep disk space above designated level	
def keepDiskSpaceFree(bytesToReserve):
	if (getFreeSpace() < bytesToReserve):
		for filename in sorted(os.listdir(".")):
			if filename.startswith("capture") and filename.endswith(".jpg"):
				os.remove(filename)
				print '[!] Deleted %s to avoid filling disk space...' % filename
				if (getFreeSpace() > bytesToReserve):
					return
					
#Get available disk space
def getFreeSpace():
	st = os.statvfs(".")
	du = st.f_bavail * st.f_frsize
    	return du

#To check if the image has a face and capture all facial attributes
def check_face(client, file):
    face_detected = False
    with open(file, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
        if (not response['FaceDetails']):
            face_detected = False
        else: 
            face_detected = True

    return face_detected, response

#Check if there is any faces that match the collection
def check_matches(client, file):
    collectionid = config.get('App Settings', 'collectionid')
    face_matches = False
    with open(file, 'rb') as image:
        response = client.search_faces_by_image(CollectionId=collectionid, Image={'Bytes': image.read()}, MaxFaces=1, FaceMatchThreshold=85)
        if (not response['FaceMatches']):
            face_matches = False
        else:
            face_matches = True

    return face_matches, response

def main():
    #args = get_args()
    client = get_client()
    imageFile = take_picture(diskSpaceToReserve)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    host_ip = s.getsockname()[0]
    fport = config.get('Webserver', 'fport')
    files = {"attachment": ("image.jpg", open(imageFile, "rb"), "image/jpeg")}
    imageURL = imageFile.replace("/home/pi/smartdb/", "http://%s:%s/") % (host_ip, fport)
    POtoken = config.get('App Settings', 'POtoken')
    POuser = config.get('App Settings', 'POuser')
    wcurl = config.get('App Settings', 'wcurl')
    ifturl = config.get('App Settings', 'ifturl')
    iftEvent = config.get('App Settings', 'iftEvent')
    
    print '[+] Getting things started...'
    
    print '[+] Processing %s...' % imageFile
    print '[+] Running face checks against image...'
    result, resp = check_face(client, imageFile)

    if (result):
        print '[+] Face(s) detected with %r confidence...' % (round(resp['FaceDetails'][0]['Confidence'], 2))
        print '[+] Checking for a face match...'
        resu, res = check_matches(client, imageFile)
    
        if (resu):
            print '[+] I am %r confident that i saw %s... - <img src=%s width=900 height=600>' % (round(res['FaceMatches'][0]['Similarity'], 1), res['FaceMatches'][0]['Face']['ExternalImageId'], imageURL)
	    matchmsg = 'I am %r confident that i saw %s... - %s' % (round(res['FaceMatches'][0]['Similarity'], 1), res['FaceMatches'][0]['Face']['ExternalImageId'], imageURL)
	 #Command to send to webCoRE.
            r = requests.post(wcurl, data={'person':res['FaceMatches'][0]['Face']['ExternalImageId'], 'similarity':round(res['FaceMatches'][0]['Similarity'], 2), 'confidence':round(res['FaceMatches'][0]['Face']['Confidence'], 2), 'faceConfidence':round(resp['FaceDetails'][0]['Confidence'], 2), 'ageHigh':resp['FaceDetails'][0]['AgeRange']['High'], 'ageLow':resp['FaceDetails'][0]['AgeRange']['Low'], 'gender':resp['FaceDetails'][0]['Gender']['Value'], 'genderConf':round(resp['FaceDetails'][0]['Gender']['Confidence'], 2), 'mustache':resp['FaceDetails'][0]['Mustache']['Value'], 'sunglasses':resp['FaceDetails'][0]['Sunglasses']['Value']})
	 #Command to send to Pushover.
	    r = requests.post("https://api.pushover.net/1/messages.json", data = {"token": POtoken, "user": POuser, "message": imageURL}, files = files)
	 #Command to send to IFTTT. 
	    r = requests.post(ifturl, data={'event':iftEvent, 'value1':matchmsg})
        else:
            print '[-] I detect a %s between the age of %s - %s. Mustache - %s, Sunglasses - %s... - <img src=%s width=900 height=600>' % (resp['FaceDetails'][0]['Gender']['Value'], resp['FaceDetails'][0]['AgeRange']['Low'], resp['FaceDetails'][0]['AgeRange']['High'], resp['FaceDetails'][0]['Mustache']['Value'], resp['FaceDetails'][0]['Sunglasses']['Value'], imageURL)
	    nomatchmsg = 'I detect a %s between the age of %s - %s. Mustache - %s, Sunglasses - %s... %s' % (resp['FaceDetails'][0]['Gender']['Value'], resp['FaceDetails'][0]['AgeRange']['Low'], resp['FaceDetails'][0]['AgeRange']['High'], resp['FaceDetails'][0]['Mustache']['Value'], resp['FaceDetails'][0]['Sunglasses']['Value'], imageURL)
	 #Command to send to webCoRE.
            r = requests.post(wcurl, data={'person':'Unknown', 'faceConfidence':round(resp['FaceDetails'][0]['Confidence'], 2), 'ageHigh':resp['FaceDetails'][0]['AgeRange']['High'], 'ageLow':resp['FaceDetails'][0]['AgeRange']['Low'], 'gender':resp['FaceDetails'][0]['Gender']['Value'], 'genderConf':round(resp['FaceDetails'][0]['Gender']['Confidence'], 2), 'mustache':resp['FaceDetails'][0]['Mustache']['Value'], 'sunglasses':resp['FaceDetails'][0]['Sunglasses']['Value']})
	 #Command to send to Pushover.
	    r = requests.post("https://api.pushover.net/1/messages.json", data = {"token": POtoken, "user": POuser, "message": imageURL}, files = files)
	 #Command to send to IFTTT.
	    r = requests.post(ifturl, data={'event':iftEvent, 'value1':nomatchmsg})

    else :
        print "[-] No faces detected... - <img src=%s width=900 height=600>" % imageURL
	nofacemsg = 'No face was detected - %s' % imageURL
     #Command to send to webCoRE.
	r = requests.post(wcurl, data={'person':'No'})
     #Command to send to Pushover.
	r = requests.post("https://api.pushover.net/1/messages.json", data = {"token": POtoken, "user": POuser, "message": imageURL}, files = files)
     #Command to send to IFTTT.
	r = requests.post(ifturl, data={'event':iftEvent, 'value1':nofacemsg})
if __name__ == '__main__':
    main()
