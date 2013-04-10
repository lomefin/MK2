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
from google.appengine.api import mail
import random
import string	

class LogoutHandler(mkhandler.MKHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		self.session.terminate()
		try:
		  self.response.headers.add_header('Set-Cookie','__utmc=0; expires:Sun, 31-May-2009 23:59:59 GMT; path=/;')
		except:
		  pass
		self.redirect("/login")
		
class SignupHandler(mkhandler.MKHandler):
	def base_directory(self):
		return os.path.dirname(__file__)

	def get(self):
		self.internal_get()

	def internal_get(self):
		self.render('signup')	

	def get_default_class(self):
		school = MKSchool.all().get()
		if school is None:
			school = MKSchool()
			school.name = 'Default School'
			school.put()
		mkclass = school.school_classes.get()
		if mkclass is None:
			mkclass = MKClass()
			mkclass.name = "Default Class"
			mkclass.year = 2013
			mkclass.school = school
			mkclass.put()
		return mkclass
	def internal_post(self):

		student_name = self.request.get('student_name')
		student_surname = self.request.get('student_surname')
		student_email = self.request.get('student_email')

		if len(student_name) == 0 or len(student_surname) == 0:
			self.redirect('/signup')
		#Generate a username
		username = student_name + student_surname.replace(' ','')[:8]
		username = username.lower()
		
		#Find if the username already exists
		existing_account = MKAccount.all().filter('system_login =',username).get()
		if existing_account:
			counter = 0
			while existing_account:
				counter = counter + 1
				existing_account = MKAccount.all().filter('system_login =',username + str(counter)).get()
			if counter > 0:
				username = username + str(counter)
		#If exists try with a secuence number
		
		student = MKAccount()
		student.name = student_name.capitalize()
		student.surname = student_surname.capitalize()
		student.system_login = username;
		
		#random password
		student.system_password = ''.join(random.sample(string.lowercase,6))
		student.put()
		
		mkstudent = MKStudent()
		mkstudent.student_account = student
		mkstudent.has_started = False
		mkstudent.attending_class = self.get_default_class()
		mkstudent.put()

		body = "Hola " + student_name
		body = body + "\nTe acabas de crear una cuenta en MeKuido.info! Que bacán! Tus datos son"
		body = body + "\nNombre de usuario: " + str(username)
		body = body + "\nContraseña: " + str(student.system_password)
		body = body + "\nEntra a http://mekuido.info cuantas veces quieras!"

		mail.send_mail(sender="MeKuido <hola@mekuido.info>",
              to=student_email,
              subject="Tu cuenta de MeKuido!",
              body=body)

		self.current_account = student
		self.current_student_user = mkstudent
		self.current_account.last_entrance = datetime.datetime.now()
		self.current_account.put()
		self.session["current_student_user"] = self.current_student_user
		self.session["current_student_user"].put()

		self.session["current_account"] = self.current_account
		self.session["current_account"].put()
		time.sleep(1)

		self.redirect('/start/')
						

class DefaultHandler(mkhandler.MKHandler):
		
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self):
		self.internal_get()
		
	def internal_get(self):
		values = {'flash_message' : 'Problemas'}
		values = {}
		self.render('index',template_values=values)
		#self.base_auth()
		#self.get_internal()
		#user_logout = users.create_logout_url("/eventos/")
		#self.response.out.write("<a href=\"%s\">Logout</a>." %user_logout)

	def internal_post(self):
		
		#Look up for the username
		self.current_account =  MKAccount.all().filter('system_login = ',self.request.get('username')).filter('system_password = ',self.request.get('password')).get()
		
		if not self.current_account:
			values = {'flash' : 'Nombre de usuario o contrasena no existe'}
			self.render('index',template_values=values)
			return
		
		#The user exist, now must check if it is a student.
		self.current_student_user = MKStudent.all().filter('student_account = ',self.current_account).get()
		self.current_account.last_entrance = datetime.datetime.now()
		self.current_account.put()
		#Setting the session data
		#self.session.regenerate_id()
		self.session["current_account"] = self.current_account
		self.session["current_account"].put()
		time.sleep(1)
		
		
		if self.current_student_user:
			self.session["current_student_user"] = self.current_student_user
			self.session["current_student_user"].put()
			time.sleep(1)
			#Check if it has started
			if self.current_student_user.has_started:
				self.redirect('/')
				return
			else:
				self.redirect('/start/')
				return
		
		self.redirect('/teacher_panel/')
		
def main():
  application = webapp.WSGIApplication([('/login', DefaultHandler),('/logout', LogoutHandler),('/signup',SignupHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
