#!/usr/bin/env python3
from bottle import route,  get, post, request, run, template, abort # $ pip install bottle
from gevent import monkey; monkey.patch_all()
import sys, os, requests
import urllib
import urllib.parse
import urllib.request

token=os.getenv('TG_TOKEN') or ''
port=os.getenv('TGAPI_PORT') or '8001'
auth_key=os.environ.get('API_AUTHKEY') or 'p@ssw0rd'
limit = 3000

def text_splitter(text, limit):
    return [text[i: i + limit] for i in range(0, len(text), limit)]


def sendText(chat,text):
    url = "https://api.telegram.org/bot"+token+"/sendMessage";
    data = {'chat_id' : chat, 'text': text}
    try:
        r= requests.post(url, data=data, timeout=10)
        print(r.status_code, r.reason, r.content)
        data= " status: "+str(r.status_code)+" reason:"+ str(r.reason) +" content:"+ str(r.content)
        return data
    except Exception as e:
        raise e

@post('/message') # or @route('/message', method='POST')
def login_submit():
    dict = request.forms
    text=''
    for key in dict:
        text=text+"\n"+key+": "+dict[key]
    akey = request.query.key
    recepient = request.query.recepient
    if akey == auth_key:
    	for txt in text_splitter(text,limit):
           sendText(recepient,txt)
    else:
    	abort(403, "NOAUTH")
    #return template('{{data}}', data=text )

@post('/messagev2') # or @route('/message', method='POST')
def login_submit():
    dict = request.forms
    text=''
    for key in dict:
        if key != 'key' and key != 'recepient':
            text=text+"\n"+key+": "+dict[key]
    akey = request.forms.get('key')
    recepient = request.forms.get('recepient')
    if akey == auth_key:
        for txt in text_splitter(text,limit):
           sendText(recepient,txt)
    else:
        abort(403, "NOAUTH")
    #return template('{{data}}', data=text )


run(host='', port=port, server='gevent')
