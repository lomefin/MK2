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
import datetime
from model.models import *
import random
import string			

class ListStudentHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,second_argument):
		self.auth_check()
		self.internal_get(second_argument)
	
	def internal_get(self,class_id):
		
		classes = MKClass.get_by_id(int(class_id))
		students_in_class = classes.class_students.fetch(100)
		
		students_in_class.sort(cmp=lambda x,y: cmp(x.student_account.surname,y.student_account.surname))
		students = students_in_class
		values = {
			'class':classes,
			'students':students
		}
		
		self.render('list_student',template_values=values)
	
	def post(self,second_argument):
		self.auth_check()
		self.internal_post(second_argument)
	
	def internal_post(self,class_id):
		student = MKStudent.get_by_id(int(self.request.get('student_id')))
		new_class = MKClass.get_by_id(int(self.request.get('switch_class')))
		
		student.attending_class = new_class
		student.put()
		
		self.set_flash('El alumno ha sido movido')
		self.redirect('/admin/students/'+class_id+'/list')

class ListStudentReportHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,second_argument):
		self.auth_check()
		self.internal_get(second_argument)
	def post(self,second_arg):
		self.auth_check()
		self.internal_get(second_arg)
	
	def internal_get(self,class_id):
		
		classes = MKClass.get_by_id(int(class_id))
		students_in_class = classes.class_students.fetch(100)
		
		date_from = self.request.get('startdate_holder')
		date_to = self.request.get('enddate_holder')
		
		if date_from is None or date_from == '':
		  date_from = datetime.datetime.today() - datetime.timedelta(days=7)
		else:
		  date_from = datetime.datetime(*time.strptime(date_from, "%d/%m/%Y")[0:5])
		if date_to is None or date_to == '':
		  date_to = datetime.datetime.now()
		else:
		  date_to = datetime.datetime(*time.strptime(date_to, "%d/%m/%Y")[0:5])
		  
		
		students_in_class.sort(cmp=lambda x,y: cmp(x.student_account.surname,y.student_account.surname))
		students = students_in_class
		student_data_list = []
		for s in students:
		  student_data = {}
		  student_data['student'] = s
		  food_log_query = db.GqlQuery("SELECT * FROM MKDailyFoodLog WHERE creation_date > :1 and creation_date < :2 and created_by = :3",date_from,date_to,s.student_account)
		  student_data['foodlogs'] = food_log_query.count()
		  trivia_query = db.GqlQuery("SELECT * FROM MKTriviaAnswer WHERE creation_date > :1 and creation_date < :2 and answered_by = :3",date_from,date_to,s)
		  student_data['trivias'] = trivia_query.count()
		  accesses_query = db.GqlQuery("SELECT * FROM MKAccess WHERE creation_date > :1 and creation_date < :2 and student = :3",date_from,date_to,s)
		  student_data['accesses'] = accesses_query.count()
		  todo_query = db.GqlQuery("SELECT * FROM MKGoal WHERE creation_date > :1 and creation_date < :2 and created_by = :3",date_from,date_to,s.student_account)
		  student_data['todos'] = todo_query.count()
		  
		  student_data_list.append(student_data)
		
		values = {
			'class':classes,
			'students':students,
			'data_list':student_data_list,
			'date_from' : date_from.isoformat(),
			'date_to' : date_to.isoformat(),
			'days' : range(1,32),
			'months' : range(1,13),
			'years' : range(2010,2012)
		}
		
		self.render('list_student_report',template_values=values)


class ListStudentMooreHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def post(self,second_argument):
		self.auth_check()
		self.internal_post(second_argument)
	
	def get(self,second_argument):
		self.auth_check()
		self.internal_get(second_argument)
	
	def internal_get(self,class_id):
		
		classes = MKClass.get_by_id(int(class_id))
		students_in_class = classes.class_students.fetch(100)
		
		students_in_class.sort(cmp=lambda x,y: cmp(x.student_account.surname,y.student_account.surname))
		for student in students_in_class:
		  if student.moore_results.count()== 0:
		    mkmr = MKMooreResult()
		    mkmr.student = student
		    mkmr.put()
		
		students = students_in_class
		values = {
			'class':classes,
			'students':students
		}
		
		self.render('list_student_moore',template_values=values)
	def internal_post(self,class_id):
		
		classes = MKClass.get_by_id(int(class_id))
		students_in_class = classes.class_students.fetch(100)
		
		students_in_class.sort(cmp=lambda x,y: cmp(x.student_account.surname,y.student_account.surname))
		for student in students_in_class:
		  mkmr = student.moore_results[0]
		  mkmr.item42 = int(self.request.get('item42for'+str(student.key().id())))
		  mkmr.item12 = int(self.request.get('item12for'+str(student.key().id())))
		  mkmr.item13 = int(self.request.get('item13for'+str(student.key().id())))
		  mkmr.item17 = int(self.request.get('item17for'+str(student.key().id())))
		  mkmr.put()
		
		students = students_in_class
		values = {
			'class':classes,
			'students':students
		}
		self.set_flash('Cambios guardados')
		self.render('list_student_moore',template_values=values)

class ListStudentSimpleHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,second_argument):
		self.auth_check()
		self.internal_get(second_argument)
	
	def internal_get(self,class_id):
		
		classes = MKClass.get_by_id(int(class_id))
		students_in_class = classes.class_students.fetch(100)
		
		students_in_class.sort(cmp=lambda x,y: cmp(x.student_account.surname,y.student_account.surname))
		students = students_in_class
		values = {
			'class':classes,
			'students':students
		}
		
		self.render('list_student_simple',template_values=values)
	



class ChangeNutritionalStatusHandler(mkhandler.MKGAEHandler):
  
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def post(self,second_argument):
		self.auth_check()
		self.internal_post(second_argument)
		
	def internal_post(self,class_id):
		try:
		  student = MKStudent.get_by_id(int(self.request.get('student_id')))
		  
		  newNutritionalStatus = self.request.get('check_nutritional_status')
		  
		  student.student_nutritional_status = newNutritionalStatus
		  
		  student.put()
		  self.set_flash('El estado nutricional ha sido cambiado a ' + newNutritionalStatus)
		except Exception,e:
		  self.set_flash('Error, ' + str(e))
		  
		self.redirect('/admin/students/'+class_id+'/list')
	  
class StudentLoginChangeHandler(mkhandler.MKGAEHandler):
  
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,second_argument):
		self.auth_check()
		self.internal_get(second_argument)
	
	def internal_get(self,class_id):
		student = MKStudent.get_by_id(int(class_id))
		
		values = {'student':student}
		
		self.render('change_student_login',template_values=values)
		
	def post(self,second_argument):
		self.auth_check()
		self.internal_post(second_argument)
		
	def internal_post(self,student_id):
		try:
		  student = MKStudent.get_by_id(int(student_id))
		  
		  newUsername = self.request.get('new_login')
		  
		  #Find if the username already exists
		  existing_account = MKAccount.all().filter('system_login =',newUsername).get()
		  if existing_account:
			counter = 0
			while existing_account:
				counter = counter + 1
				existing_account = MKAccount.all().filter('system_login =',newUsername + str(counter)).get()
			if counter > 0:
				newUsername = newUsername + str(counter)
		  
		  student.student_account.system_login = newUsername
		  
		  student.student_account.put()
		  student.put()
		
		  self.set_flash('Nombre de usuario cambiado a ' + newUsername)
		
		  self.redirect('/admin/students/'+str(student.attending_class.key().id())+'/list')
		except Exception,e:
		  self.set_flash('No se pudo cambiar el nombre de usuario '+str(e),'error_flash')
		  self.redirect('/admin/students/'+str(student.attending_class.key().id())+'/list')

class ViewStudentHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,second_argument):
		self.auth_check()
		self.internal_get(second_argument)
	
	def internal_get(self,student_id):
	   student = MKStudent.get_by_id(int(student_id))
	   values = {'student':student}
	   self.render('view_student',template_values=values)

class AddStudentHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,second_argument):
		self.auth_check()
		self.internal_get(second_argument)
	
	def internal_get(self,class_id):
		
		#self.base_auth()
		#self.get_internal()
		#user_logout = users.create_logout_url("/eventos/")
		#self.response.out.write("<a href=\"%s\">Logout</a>." %user_logout)
		classes = MKClass.get_by_id(int(class_id))
		
		values = {
			'user_count_range':range(1,51),
			'class' : classes
		}
		
		self.render('add_student',template_values=values)
	
	def post(self,second_argument):
		self.auth_check()
		self.internal_post(second_argument)
	
	def internal_post(self,class_id):
		
		flash_message = ''
		mkclass = MKClass.get_by_id(int(class_id))
		users_created = []
		for i in range(1,51):
			student_name = self.request.get('student_name'+str(i))
			student_surname = self.request.get('student_surname' + str(i))
			
			if len(student_name) == 0 or len(student_surname) == 0:
				continue
			#Generate a username
			username = student_name[0] + student_surname.replace(' ','')[:8]
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
			mkstudent.attending_class = mkclass
			mkstudent.put()
			
			users_created.append(student)
			
				
			
		flash_message = 'Usuarios creados exitosamente'
			
		values = {
					'flash' : flash_message,
					'created_users' : users_created,
					'class' : mkclass
					
				}
		
		self.render('added_student',template_values=values)

def main():
  application = webapp.WSGIApplication([('/admin/students/(\d*)/add', AddStudentHandler),
					('/admin/students/(\d*)/changelogin',StudentLoginChangeHandler),
					('/admin/students/(\d*)/list',ListStudentHandler),
					('/admin/students/(\d*)/list/simple',ListStudentSimpleHandler),
					('/admin/students/(\d*)/list/report',ListStudentReportHandler),
					('/admin/students/(\d*)/list/moore',ListStudentMooreHandler),
					('/admin/students/(\d*)/change_nutritional_status',ChangeNutritionalStatusHandler),
					('/admin/students/(\d*)/view',ViewStudentHandler)
										],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
