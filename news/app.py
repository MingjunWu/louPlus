#! /usr/bin/env python3
from flask import Flask, render_template,abort
import json, os
app = Flask(__name__)

@app.route('/')
def index():
    i = 0
    js_text = [1,2]
    path_for_json = '/home/shiyanlou/files/'
    json_files = [ps_json for ps_json in os.listdir(path_for_json) if ps_json.endswith('.json')]
    for js in json_files:
        with open(os.path.join(path_for_json, js)) as jsfile:
            js_text[i] = json.load(jsfile)
            i+=1
    return render_template('index.html',js_text=js_text)
@app.route('/files/<filename>')
def file(filename):
    path_for_json = '/home/shiyanlou/files/'
    try: 
        filename = filename +'.json'
        with open(os.path.join(path_for_json, filename)) as jsfile:
            js_text = json.load(jsfile)
    except FileNotFoundError:
        abort(404)
    return render_template('file.html',js_text = js_text)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404        

