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
from lib.calorie_analysis import *

class DefaultHandler(mkhandler.MKHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		imc = IMCCalculator()
		imc.check_imc_of_student(self.current_student_user)
		if self.current_student_user is not None and self.current_student_user.student_nutritional_status is not None:
		    imc.status = self.current_student_user.student_nutritional_status 
		else:
		    try:
		      self.current_student_user.student_nutritional_status = imc.status
		      self.current_student_user.put()
		    except:
		      pass
		
		notification_data = None
		try:
		  if self.current_student_user.moore_results.count() > 0:
		    notification_data = 'Revisa los resultados de tu encuesta <a href="/moore/" style="color:white">Revisalos!</a>'
		except:
		  pass
		if self.current_student_user and self.current_student_user.student_avatar:
		 	kid_data = self.current_student_user.student_avatar.sex + "-" + self.current_student_user.student_avatar.prefix + "-stand"
			self.render('index_old',template_values={'imc_calc':imc,'kid_data':kid_data,'show_kid': True,'bubble_data':'¿Necesitas ayuda?','notification_data':notification_data})
		else:
			self.render('index_old',template_values={'imc_calc':imc,'notification_data':notification_data})
		#self.base_auth()
		#self.get_internal()
		#user_logout = users.create_logout_url("/eventos/")
		#self.response.out.write("<a href=\"%s\">Logout</a>." %user_logout)


def main():
  application = webapp.WSGIApplication([('/', DefaultHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
