#!/usr/bin/env python

import boto3 as b3
import StringIO
from time import gmtime, strftime
import requests
from collections import OrderedDict
import json
import os
import time
import subprocess
from datetime import datetime

#File Settings
diskSpaceToReserve = 40 * 1024 * 1024 #Keep 40mb free on disk
 
def get_client():
    return b3.client('rekognition')

#Takes a picture and names it    
def take_picture(diskSpaceToReserve):
	keepDiskSpaceFree(diskSpaceToReserve)
	time = datetime.now()
	filename = "/home/pi/smartdb/static/capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)

	print '[+] A photo is being taken now...'

	subprocess.call("raspistill -o %s --timeout 1 --nopreview --exposure sports -w 800 -h 600" % filename, shell=True)
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
    face_matches = False
    with open(file, 'rb') as image:
        response = client.search_faces_by_image(CollectionId='myfamily', Image={'Bytes': image.read()}, MaxFaces=1, FaceMatchThreshold=85)
        if (not response['FaceMatches']):
            face_matches = False
        else:
            face_matches = True

    return face_matches, response

def main():
    #args = get_args()
    client = get_client()
    imageFile = take_picture(diskSpaceToReserve)
    files = {"attachment": ("image.jpg", open(imageFile, "rb"), "image/jpeg")}
    imageURL = imageFile.replace("/home/pi/smartdb/", "http://10.14.122.66:5000/")
    #POtoken = <your Pushover Token>
    #POuser = <your Pushover User Key>
    url = 'https://graph-eu01-euwest1.api.smartthings.com/api/token/c2803a67-4113-461d-ab6f-86f6dc2fb83b/smartapps/installations/4f0cc750-2e01-4ef1-a74e-39621749016a/execute/:b7c8603f323b84d7c8a10ba49ff677a2:'
    
    print '[+] Getting things started...'
    
    print '[+] Processing %s...' % imageFile
    print '[+] Running face checks against image...'
    result, resp = check_face(client, imageFile)

    if (result):
        print '[+] Face(s) detected with %r confidence...' % (round(resp['FaceDetails'][0]['Confidence'], 2))
        print '[+] Checking for a face match...'
        resu, res = check_matches(client, imageFile)
    
        if (resu):
            print '[+] Identity matched %s with %r similarity and %r confidence...' % (res['FaceMatches'][0]['Face']['ExternalImageId'], round(res['FaceMatches'][0]['Similarity'], 1), round(res['FaceMatches'][0]['Face']['Confidence'], 2))
            r = requests.post(url, data={'person':res['FaceMatches'][0]['Face']['ExternalImageId'], 'similarity':round(res['FaceMatches'][0]['Similarity'], 2), 'confidence':round(res['FaceMatches'][0]['Face']['Confidence'], 2), 'faceConfidence':round(resp['FaceDetails'][0]['Confidence'], 2), 'ageHigh':resp['FaceDetails'][0]['AgeRange']['High'], 'ageLow':resp['FaceDetails'][0]['AgeRange']['Low'], 'gender':resp['FaceDetails'][0]['Gender']['Value'], 'genderConf':round(resp['FaceDetails'][0]['Gender']['Confidence'], 2), 'mustache':resp['FaceDetails'][0]['Mustache']['Value'], 'sunglasses':resp['FaceDetails'][0]['Sunglasses']['Value']})
	    #r = requests.post("https://api.pushover.net/1/messages.json", data = {"token": "agpjf2unwji4jdozretwkcwh89jo7n", "user": "uxqAujkeFN5g1btLFoQHpnkRXM5DNX", "message": imageURL}, files = files)
        else:
            print '[-] No face matches detected...'
            r = requests.post(url, data={'person':'Unknown', 'faceConfidence':round(resp['FaceDetails'][0]['Confidence'], 2), 'ageHigh':resp['FaceDetails'][0]['AgeRange']['High'], 'ageLow':resp['FaceDetails'][0]['AgeRange']['Low'], 'gender':resp['FaceDetails'][0]['Gender']['Value'], 'genderConf':round(resp['FaceDetails'][0]['Gender']['Confidence'], 2), 'mustache':resp['FaceDetails'][0]['Mustache']['Value'], 'sunglasses':resp['FaceDetails'][0]['Sunglasses']['Value']})
	    #r = requests.post("https://api.pushover.net/1/messages.json", data = {"token": POtoken, "user": POuser, "message": imageURL}, files = files)

    else :
        print "[-] No faces detected..."
	#r = requests.post("https://api.pushover.net/1/messages.json", data = {"token": "agpjf2unwji4jdozretwkcwh89jo7n", "user": "uxqAujkeFN5g1btLFoQHpnkRXM5DNX", "message": imageURL}, files = files)
        
if __name__ == '__main__':
    main()
