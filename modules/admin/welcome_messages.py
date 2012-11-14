# -*- coding: utf-8 -*-import cgi
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import datetime
import os
import lib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import datastore_errors
from google.appengine.ext.webapp import template
from lib import mkhandler
import datetime
from model.models import *
import random
import string			

class WelcomeMessageHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		messages = MKWelcomeMessage.all().order('-is_active')
		
		values = {
			'messages':messages,
		}
		
		self.render('list_welcome_messages',template_values=values)
	
	
	def internal_post(self):
		welcome_message = MKWelcomeMessage()
		welcome_message.title = self.request.get('title')
		welcome_message.body = self.request.get('body')
		welcome_message.is_active = True
		welcome_message.put()
		self.set_flash('Se ha agregado el mensaje de bienvenida.')
		self.redirect('/admin/welcome_messages/')

class WelcomeMessageTogglerHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,key):
		self.auth_check()
		self.internal_get(key)

	def internal_get(self,message_key):
		message = MKWelcomeMessage.get(db.Key(encoded = message_key))
		m = "desactivado" if message.is_active else "activado"
		message.is_active = not message.is_active
		message.put()
		self.set_flash("El mensaje '"+message.title+"' se ha " + m + ".")
		self.redirect('/admin/welcome_messages/')
	
class WelcomeMessageRemoverHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,key):
		self.auth_check()
		self.internal_get(key)

	def internal_get(self,message_key):
		message = MKWelcomeMessage.get(db.Key(encoded = message_key))
		message.delete()
		self.set_flash("El mensaje '"+message.title+"' se ha eliminado.")
		self.redirect('/admin/welcome_messages/')
	


def main():
  application = webapp.WSGIApplication([('/admin/welcome_messages/', WelcomeMessageHandler),
  										('/admin/welcome_messages/(.*)/toggle', WelcomeMessageTogglerHandler),
  										('/admin/welcome_messages/(.*)/remove', WelcomeMessageRemoverHandler)

										],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
