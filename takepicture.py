#!/usr/bin/env python

import boto3 as b3
from argparse import ArgumentParser
from time import gmtime, strftime
import requests
from collections import OrderedDict
import json
from picamera import PiCamera
import os
import time
 
def get_client():
    return b3.client('rekognition')
    
def take_picture():
	count = 1
	camera = PiCamera()
	camera.vflip = True
	camera.hflip = True
	directory = '/home/pi/smartdb/media'

	print '[+] A photo is being taken now...'

	milli = int(round(time.time() * 1000))
	image = '{0}/image_{1}.jpg'.format(directory, milli)
	camera.capture(image)
	print '[+] Your image was saved to %s...' % image
	return image
	
def get_args():
    parser = ArgumentParser(description='Compare an image')
    parser.add_argument('-i', '--image')
    parser.add_argument('-c', '--collection')
    return parser.parse_args()

def check_face(client, file):
    face_detected = False
    with open(file, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
        if (not response['FaceDetails']):
            face_detected = False
        else: 
            face_detected = True

    return face_detected, response

def check_matches(client, file, collection):
    face_matches = False
    with open(file, 'rb') as image:
        response = client.search_faces_by_image(CollectionId='myfamily', Image={'Bytes': image.read()}, MaxFaces=1, FaceMatchThreshold=85)
        if (not response['FaceMatches']):
            face_matches = False
        else:
            face_matches = True

    return face_matches, response

def main():
    args = get_args()
    client = get_client()
    imageFile = take_picture()
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
        else:
            print '[-] No face matches detected...' 
	    r = requests.post(url, data={'person':'Unknown', 'faceConfidence':round(resp['FaceDetails'][0]['Confidence'], 2), 'ageHigh':resp['FaceDetails'][0]['AgeRange']['High'], 'ageLow':resp['FaceDetails'][0]['AgeRange']['Low'], 'gender':resp['FaceDetails'][0]['Gender']['Value'], 'genderConf':round(resp['FaceDetails'][0]['Gender']['Confidence'], 2), 'mustache':resp['FaceDetails'][0]['Mustache']['Value'], 'sunglasses':resp['FaceDetails'][0]['Sunglasses']['Value']})

    else :
        print "[-] No faces detected..."
        
if __name__ == '__main__':
    main()
