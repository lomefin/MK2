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
import string
import datetime
from model.models import *
from lib.calorie_analysis import *

class DefaultHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
		
	def internal_get(self):
		classes = MKClass.all()
		values = {'classes':classes}
		self.render('list_operations',template_values=values)

		
class CleanSessionsHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
		
	def internal_get(self):
		action = "Se borraran las Sesiones"
		values = {'action':action}
		self.render('do_operation',template_values=values)
	def internal_post(self):
		try:
			from lib.gaesessions import delete_expired_sessions
			while not delete_expired_sessions():
				pass
			self.set_flash('Sesiones limpias')
		except Exception, e:
			self.set_flash('No se pudo limpiar el sistema de sesiones (%s)'%e)
		self.render('list_operations')

class RestartStudentsHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
		
	def internal_get(self):
		action = "Se reiniciaran el estado de iniciado para los usuarios invalidos."
		values = {'action':action}
		self.render('do_operation',template_values=values)

	def internal_post(self):
		values = {}
		try:
			query = db.GqlQuery("SELECT * FROM MKStudent WHERE student_birth_date > :1",None)
			results = []
			for student in query.fetch(limit=100):
				student.has_started = False
				student.put()
				results.append( "Alumno %s reiniciado" % student.student_account.system_login)
			values['results'] = results
			self.set_flash('Alumnos reiniciados')
		except Exception, e:
			self.set_flash('No se pudo reiniciar a los alumnos (%s)'%e)
		self.render('list_operations',template_values=values)		

class ReevaluateIMCPerClass (mkhandler.MKGAEHandler):
  
	def base_directory(self):
		return os.path.dirname(__file__)
		
	def internal_get(self):
		
		mkClass = MKClass.get_by_id(int(self.request.get('class_id')))
		action = "Se recalcularan los IMC de los alumnos del curso " + mkClass.name + " del colegio " + mkClass.school.name
		values = {'action':action}
		self.render('do_operation',template_values=values)
	
	def internal_post(self):
		
		mkClass  = MKClass.get_by_id(int(self.request.get('class_id')))
		results = []
		imc = IMCCalculator()
		for student in mkClass.class_students:
			try:
			  imc.check_imc_of_student(student)
			  imcResult = imc.status
			  student.student_nutritional_status = imcResult
			  results.append(student.student_account.name+ " " +student.student_account.surname + " : " + imcResult)
			  student.put()
			except Exception,e:
			  results.append("Error con alumno " + student.student_account.name + ", Error: " + str(e))
		values={'results': results}
		self.set_flash('IMC reevaluados')
		self.redirect('/admin/scripts/')
  
class RenameICMValues (mkhandler.MKGAEHandler):
  
	def base_directory(self):
		return os.path.dirname(__file__)
		
	def internal_get(self):
		
		
		action = "Se renombraren los resultados del IMC de los alumnos"
		values = {'action':action}
		self.render('do_operation',template_values=values)
	
	def internal_post(self):
		
		students = db.Query(MKStudent).filter('student_nutritional_status=','enflaquecido')
		
		for student in students:
		  student.student_nutritional_status = 'bajo peso'
		  student.put()
		  
		students = db.Query(MKStudent).filter('student_nutritional_status=','sobrepeso') 
		
		for student in students:
		  student.student_nutritional_status = 'riesgo de obesidad'
		  student.put()
		
		self.set_flash('IMC renombrados')
		self.redirect('/admin/scripts/')

def main():
  application = webapp.WSGIApplication([
										('/admin/scripts/', DefaultHandler),
										('/admin/scripts/sessions/clean', CleanSessionsHandler),
										('/admin/scripts/students/restart', RestartStudentsHandler),
										('/admin/scripts/students/reavaluate_imc_per_class', ReevaluateIMCPerClass),
										('/admin/scripts/renameICMValues',RenameICMValues)
										],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
