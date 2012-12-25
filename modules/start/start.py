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
import time

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import datastore_errors
from google.appengine.ext.webapp import template
from lib import mkhandler
from model.models import *

class DefaultHandler(mkhandler.MKHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		if self.current_student_user.has_started:
			self.redirect('/start/chooseAvatar')
		days = range(1,32)
		months = range(1,13)
		years = range(1994,2005)
		values = { 'hide_menu' : 'hide','days':days,'months':months,'years':years}
		self.render('first_time',template_values=values)

	def internal_post(self):
		
		self.current_student_user.student_weight = float(self.request.get('weight'))
		self.current_student_user.student_height = float(self.request.get('height'))
		self.current_student_user.student_birth_date = datetime.datetime(*time.strptime(self.request.get('birth_date'), "%d/%m/%Y")[0:5])
		self.current_student_user.student_gender = self.request.get('sex')
		self.current_student_user.has_started = True
		
		self.current_student_user.put()
		self.update_session()
		time.sleep(2)
		self.redirect('/start/chooseAvatar')

		
class AvatarChooseHandler(mkhandler.MKHandler):

	def base_directory(self):
		return os.path.dirname(__file__)
		
	def internal_get(self):
		sex = 'masculino'
		avatar_list = MKAvatar.all().filter('sex = ', str(self.current_student_user.student_gender) == 'masculino')
		
		
		values = { 'hide_menu' : 'hide' , 'avatar_list' : avatar_list}
		self.render('choose_avatar',template_values=values)

class AvatarChosenHandler(mkhandler.MKHandler):
	def get(self,avatar_prefix):
		self.auth_check()
		self.internal_get(avatar_prefix)

	def internal_get(self,avatar_prefix):
		
		avatar = MKAvatar.all().filter('sex = ', str(self.current_student_user.student_gender) == 'masculino').filter('prefix =',avatar_prefix).get()
		self.current_student_user.student_avatar = avatar
		
		self.current_student_user.put()
		self.update_session()
		self.redirect('/')

def main():
  application = webapp.WSGIApplication([('/start/', DefaultHandler),
										('/start/(\D*?)/select',AvatarChosenHandler),
										('/start/chooseAvatar', AvatarChooseHandler),
										],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
