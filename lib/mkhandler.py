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
import time
import datetime
#import controller.sessions.SessionManager
#from appengine_utilities.sessions import Session
from lib.gaesessions import get_current_session
#from controller.appengine_utilities.flash import Flash
#from controller.appengine_utilities.cache import Cache
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import datastore_errors
from google.appengine.ext.webapp import template
from model.models import *

class MKGAEHandler(webapp.RequestHandler):
	def __init__(self):
		self.flash = ''
		self.flash = None
		self.flash_type = 'normalFlash'
		self.log_count = 1
		#self.auth_check()
	
	def set_flash(self,flash,flash_type='normalFlash'):
		if(self.session):
			self.session['flash'] = flash
			self.session['flash_type'] = flash_type
	
	def read_flash(self):
		if(self.session):
			if(self.session.has_key('flash')):
				self.flash = self.session.pop('flash',default=None)
				self.flash_type = self.session.pop('flash_type',default='normalFlash')	
		else:
			self.wr('NO SESSION')
			
		
	def auth_check(self):
		user = users.get_current_user()
		
		#Check if the user is in @mekuido.info
		if user:
			emailDomain = user.email().split("@")
			if emailDomain[1] == "mekuido.info":
				self.session = get_current_session()
				self.current_student_user = None
				self.current_account = None
				
				if self.session.has_key("current_account"):
					self.current_account = self.session["current_account"]	
				else:
					self.current_account = MKAccount.all().filter('email = ',user.email()).get()
					
					if not self.current_account:
						self.current_account = MKAccount()
						self.current_account.email = user.email()
						#self.current_account.put()
					#Setting the session data
					self.current_account.last_entrance = datetime.datetime.now()
					self.current_account.put()
					self.session["current_account"] = self.current_account
					#self.session["current_account"].put()
					time.sleep(1)
				return True
			else:
				self.redirect('/admin/unlog/')
				#self.redirect('/unlogFromGoogleAcount')
				
		else:
			self.redirect(users.create_login_url(self.request.uri))
        
			
	def render(self,pagename,template_values=None):
		self.logout_url = '/admin/unlog/'
		self.user_mail = ''
		if users.get_current_user():
			self.user_mail = users.get_current_user().email()
		
		if not template_values:
			template_values = {'user_mail':self.user_mail,'logout_url': self.logout_url}
		else:
			template_values['logout_url'] = self.logout_url
			template_values['user_mail'] = self.user_mail
		try:
			if self.current_account is not None:
				template_values['current_account'] = self.current_account
		except:
			pass
		try:
			self.read_flash()
			
			template_values['flash'] = self.flash
			template_values['flash_type'] = self.flash_type
		except:
			pass
			
		path = os.path.join(self.base_directory(), 'views/'+pagename+'.html')
		self.response.out.write(template.render(path, template_values))
	
	def render_specific(self,pagename,template_values=None):
		#self.wr(os.path.dirname(__file__))
		path = os.path.join(self.base_directory(), '../../templates/'+pagename)
		#self.wr(path)
		self.response.out.write(template.render(path, template_values))
	
	def wr(self,text):
		self.response.out.write(text)
	
	def param(self,param_name):
		return self.request.get(param_name)
	
	def get(self):
		self.auth_check()
		self.internal_get()
	
	def post(self):
		self.auth_check()
		self.internal_post()

class MKEGAEHandler(MKGAEHandler):
	def auth_check(self):
		user = users.get_current_user()
		
		#Check if the user is in @mekuido.info
		self.wr('emailDomain')
		if user:
			emailDomain = user.email().split("@")
			if emailDomain[1] == "mekuido.info":
				self.session = get_current_session()
				self.current_student_user = None
				self.current_account = None
				
				if self.session.has_key("current_account"):
					self.wr('Current: ' + str(self.session["current_account"]))
					self.current_account = self.session["current_account"]	
				else:
					self.current_account = MKAccount.all().filter('email = ',user.email()).get()
					self.wr( 'user email '+ str(user.email()))
					if not self.current_account:
						self.current_account = MKAccount()
						self.current_account.email = user.email()
						self.current_account.put()
					#Setting the session data
					self.session["current_account"] = self.current_account
					self.session["current_account"].put()
					time.sleep(1)
				self.flash_message = "HELO"
				self.render('index')
				return True
			else:
				self.redirect(users.create_logout_url('/admin/'))
				#self.redirect('/unlogFromGoogleAcount')
				
		else:
			self.redirect(users.create_login_url(self.request.uri))

	
	

class MKHandler(webapp.RequestHandler):
	def __init__(self):
		self.flash = ''
		self.flash = None
		self.flash_type = 'normalFlash'
		self.log_count = 1
		#self.auth_check()
	
	def set_flash(self,flash,flash_type='normalFlash'):
		if(self.session):
			self.session['flash'] = flash
			self.session['flash_type'] = flash_type

	def read_flash(self):
		if(self.session):
			if(self.session.has_key('flash')):
				self.flash = self.session.pop('flash',default=None)
				self.flash_type = self.session.pop('flash_type',default='normalFlash')
	
	def auth_check(self):
		self.session = get_current_session()
		self.current_student_user = None
		self.current_account = None
		#google_app_user = users.get_current_user()
		if self.session.has_key("current_student_user") and self.session["current_student_user"] is not None and self.session["current_student_user"] != "":
			self.current_student_user = self.session["current_student_user"]
		elif self.session.has_key("current_account") and self.session["current_account"] is not None and self.session["current_account"].system_login is not None:
			self.current_account = self.session["current_account"]	
		else:
			#Not logged in
			self.redirect('/login')
			return
	def update_session(self):
		if(self.current_student_user) : 
			self.session["current_student_user"] = self.current_student_user
		if(self.current_account):
			self.session["current_account"]	= self.current_account
		
			
	def render(self,pagename,template_values=None):
	
		self.logout_url = '/logout'
		if not template_values:
			template_values = {'logout_url': self.logout_url}
		else:
			template_values['logout_url'] = self.logout_url
		try:
			if self.session.has_key("current_account"):
				template_values['current_account'] = self.session["current_account"]
		except:
			pass
		try:
			self.read_flash()
			template_values['flash'] = self.flash
			template_values['flash_type'] = self.flash_type
			
		except:
			pass
		path = os.path.join(self.base_directory(), 'views/'+pagename+'.html')
		self.response.out.write(template.render(path, template_values))
	
	def render_specific(self,pagename,template_values=None):
		#self.wr(os.path.dirname(__file__))
		path = os.path.join(self.base_directory(), '../../templates/'+pagename)
		#self.wr(path)
		self.response.out.write(template.render(path, template_values))
	
	def wr(self,text):
		self.response.out.write(text)
	
	def param(self,param_name):
		return self.request.get(param_name)
	
	def get(self):
		self.auth_check()
		self.internal_get()
	
	def post(self):
		self.auth_check()
		self.internal_post()
		

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
