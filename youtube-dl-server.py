from __future__ import unicode_literals
import json
import os
import subprocess
from queue import Queue
import bottle
from bottle import route, run, Bottle, request, response, static_file
import youtube_dl
from pathlib import Path
from collections import ChainMap

# class EnableCors(object):
#     name = 'enable_cors'
#     api = 2

#     def apply(self, fn, context):
#         def _enable_cors(*args, **kwargs):
#             # set CORS headers
#             response.headers['Access-Control-Allow-Origin'] = '*'
#             response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
#             response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

#             if bottle.request.method != 'OPTIONS':
#                 # actual request; reply with the actual response
#                 return fn(*args, **kwargs)

#         return _enable_cors

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

@app.route('/')
def root():
    return static_file('index.html', root='./')

@app.route('/youtube-dl')
def index():

    try:
        url = request.query['url']
    except:
        return {"success": False, "error": "called without a 'url' query param"}

    try:
        options = request.query['options']
    except:
        options = {
            'format': 'best'
        }
  
    results = download(url, options)
    return results

    #return static_file('index.html', root='./')


# @app.route('/youtube-dl', method='POST')
# def q_request():
#     url = request.forms.get("url")

#     options = {
#         'format': request.forms.get("format")
#     }

#     if not url:
#         return {"success": False, "error": "called without a 'url' query param"}

#     #print("Requesting information from URL: " + url + ".")
#     #print(options)

#     response.headers['Content-type'] = 'application/json'
#     response.set_header('Access-Control-Allow-Origin', '*')
#     response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')

#     #key = request.get.GET('key')
#     #if key == "d<54a(2)tHLV[&jS":        
#     results = download(url, options)
#     #return results
#     #    else:
#     #return {"status": "Access Deny"}


@app.route("/youtube-dl/update", method="GET")
def update():
    command = ["pip", "install", "--upgrade", "youtube-dl"]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = proc.communicate()
    return {
        "output": output.decode('ascii'),
        "error":  error.decode('ascii')
    }

# def my_hook(d):
#     if d['status'] == 'finished':
#         print (d)

def download(url, request_options):
    ydl_opts = {
        'format': 'best',
        'logger': MyLogger()
        #'forcejson': True,
        #'dump_single_json': True,
        #'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url,download=False # We just want to extract the info
    )

    #print (result)
    return result


print("updating youtube-dl to the newest version...")
updateResult = update()
print(updateResult["output"])
print(updateResult["error"])

app_vars = ChainMap(os.environ, app_defaults)

#app.install(EnableCors())

port = int(os.environ.get('PORT', 80))

app.run(host=app_vars['APP_SERVER_HOST'], port=port, debug=True)
