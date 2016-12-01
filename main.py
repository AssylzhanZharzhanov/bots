# -*- coding: utf-8 -*-
import StringIO
import json
import logging
import random
import urllib
import urllib2
 
# for sending images
from PIL import Image
import multipart
 
# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2
 
TOKEN = '320293798:AAE3L8M0w2rsQvO8Wym6AFDm2He8mwBwmZM'
 
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'
 
 
class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)
 
 
def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()
 
def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False
 
class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))
 
 
class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))
 
 
class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))
 
class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))
 
        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']
 
        if not text:
            logging.info('no text')
            return

        def reply(msg=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode(),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            else:
                logging.error('No message')
                resp = None
 
            logging.info('send response:')
            logging.info(resp)
 
        if text.startswith('/'):
            if text == '/start':
                reply('Welcome')
                setEnabled(chat_id, True)
            elif text == '/help':
                reply('Enter your scores:')
                setEnabled(chat_id, True)
            else:
                reply('Wrong input')
 
        # CUSTOMIZE FROM HERE

        elif 'asd' in text:
            reply('asd')
        else:
            logging.info('not enabled for chat_id {}'.format(chat_id))

          # if text == '/calculate':
          #   reply('Enter the first number')
          #   a = msg.read()





app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
