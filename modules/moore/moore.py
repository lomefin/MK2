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
#import controller.sessions.SessionManager
#from controller.appengine_utilities.sessions import Session
#from controller.appengine_utilities.flash import Flash
#from controller.appengine_utilities.cache import Cache
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
		show_kid = False
		kid_data = None
		if self.current_student_user and self.current_student_user.student_avatar:
		 	kid_data = self.current_student_user.student_avatar.sex + "-" + self.current_student_user.student_avatar.prefix + "-stand"
		 	show_kid = True
		 	
		values = {'moore':self.current_student_user.moore_results[0],
			  'bubble_data':'Revisa tus resultados',
			  'kid_data':kid_data,
			  'show_kid':show_kid}
		
		self.render('index',template_values=values)
	

def main():
  application = webapp.WSGIApplication([('/moore/', DefaultHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
