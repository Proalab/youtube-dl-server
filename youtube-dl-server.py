from __future__ import unicode_literals
import json
import os
import subprocess
from queue import Queue
from bottle import route, run, Bottle, request, static_file
from threading import Thread
import youtube_dl
from pathlib import Path
from collections import ChainMap

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


app = Bottle()


app_defaults = {
    'APP_SERVER_HOST': '0.0.0.0',
    'APP_SERVER_PORT': 80,
}


@app.route('/youtube-dl')
def index():
    return static_file('index.html', root='./')

@route('/runcmd/<cmd>')
def cmdRunner(cmd):
    msg = subprocess.getstatusoutput(cmd)
    return printAndBack(msg)

def printAndBack(msg):
    fnc = "function pageInit() { alert('job success'); history.back(); }"
    return "<html><body onload='pageInit()'><p></p> </body> <script> "+fnc+" </script></html>"


@app.route('/youtube-dl', method='POST')
def q_request():
    url = request.forms.get("url")

    options = {
        'format': request.forms.get("format")
    }

    if not url:
        return {"success": False, "error": "called without a 'url' query param"}

    print("Requesting information from URL: " + url + ".")
    download(url, options)

    return {"success": True, "url": url, "options": options}


@app.route("/youtube-dl/update", method="GET")
def update():
    command = ["pip", "install", "--upgrade", "youtube-dl"]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = proc.communicate()
    return {
        "output": output.decode('ascii'),
        "error":  error.decode('ascii')
    }

def my_hook(d):
    if d['status'] == 'finished':
        print (d)

def download(url, request_options):
    ydl_opts = {
        'format': 'best',
        'logger': MyLogger(),
        'forcejson': True,
        'dump_single_json': True,
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


print("Updating youtube-dl to the newest version")
updateResult = update()
print(updateResult["output"])
print(updateResult["error"])

app_vars = ChainMap(os.environ, app_defaults)

app.run(host=app_vars['APP_SERVER_HOST'], port=app_vars['APP_SERVER_PORT'], debug=True)
