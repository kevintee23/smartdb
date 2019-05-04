import subprocess
import os

from flask import Flask
app = Flask(__name__)

@app.route('/')
def speedTest():
   return subprocess.Popen('./takepicture.py', shell=True, stdout=subprocess.PIPE).stdout.read()

@app.route('/smartdb/static/')
@app.route('/smartdb/static/<name>')
def hello(name=None):
    return render_template('picture.html', name=name)
