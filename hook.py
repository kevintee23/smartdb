import subprocess
import os
from flask import render_template

from flask import Flask
app = Flask(__name__)

#Will execute the takepicture.py script when x.x.x.x:5000 is accessed
@app.route('/')
def speedTest():
   return subprocess.Popen('./takepicture.py', shell=True, stdout=subprocess.PIPE).stdout.read()

#Will display the captured pic - this is to work with Pushover notification where the pic will be displayed in the notification.
@app.route('/smartdb/static/')
@app.route('/smartdb/static/<name>')
def hello(name=None):
    return render_template('picture.html', name=name)

#Will display all captured images by accessing x.x.x.x:5000/media
@app.route('/media')
def media():
	hists = sorted(os.listdir('/home/pi/smartdb/static'), reverse=True)
	hists = [file for file in hists]
	return render_template('gallery.html', hists=hists)
