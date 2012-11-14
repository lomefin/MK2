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
from lib.calorie_analysis import *
import logging
class DefaultHandler(mkhandler.MKHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		template_values = {}
		notification_data = None
		welcome_message = MKWelcomeMessage.all().filter('is_active = ',True).get()
		template_values.update({'notification_data':notification_data,'welcome_message':welcome_message})
		if self.current_student_user and self.current_student_user.student_avatar:
		 	kid_data = self.current_student_user.student_avatar.sex + "-" + self.current_student_user.student_avatar.prefix + "-stand"
		 	template_values.update({'kid_data':kid_data,'show_kid': True,'bubble_data':'¿Necesitas ayuda?'})
		self.render('index',template_values=template_values)

def main():
  application = webapp.WSGIApplication([('/', DefaultHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
