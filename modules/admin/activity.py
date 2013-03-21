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

class AddQuestionHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self, second_argument):
		self.auth_check()
		self.internal_get(second_argument)
	
	def internal_get(self,activity_code):
		values = {
			'range4' : range(4),
			'activity_code' : activity_code,
		}
		self.set('activity', MKActivity.get_by_id(int(activity_code)))
		self.render('add_activity_question',template_values=values)
		#self.base_auth()
		#self.get_internal()
		#user_logout = users.create_logout_url("/eventos/")
		#self.response.out.write("<a href=\"%s\">Logout</a>." %user_logout)

	def post(self, second_argument):
		self.auth_check()
		self.internal_post(second_argument)
		
	def internal_post(self,activity_code):
	
		activity = MKActivity.get_by_id(int(activity_code))
		
		question = MKActivityQuestion()
		question.question_text = self.request.get('question_text')
		question.general_feedback = self.request.get('feedback_text')
		question.phrase = self.request.get('phrase_text')
		question.activity = activity
		question.last_displayed = datetime.datetime.now()
		try:
			question.created_by = self.current_account
		except:
			pass
		question.put()
		self.flash = 'Pregunta Agregada'
		for i in range(4):
			possible_answer = MKActivityPossibleAnswer()
			possible_answer.possible_answer_text = self.request.get('alternative'+str(i)+'_text')
			possible_answer.feedback_text = self.request.get('feedback'+str(i)+'_text')
			possible_answer.is_correct = self.request.get('correct_alternative'+str(i)) == "True"
			possible_answer.question = question
			possible_answer.put()

		self.set_flash('Pregunta agregada a ' + activity.name)
		self.redirect('/admin/activity/'+str(activity_code)+'/listQuestions')

class ListActivityQuestionsHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self, second_argument):
		self.auth_check()
		self.internal_get(second_argument)

	def internal_get(self,activity_code):
		activity = MKActivity.get_by_id(int(activity_code))
		questions = activity.questions
		self.set('activity',activity)
		self.set('questions',questions)
		self.render('activity_list')

class ListActivityHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		activitys = MKActivity.all()
		self.set('activities',activitys)
		self.render('list_activity')

class RemoveQuestionHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	def get(self,question_code):
		self.auth_check()
		self.internal_get(question_code)

	def internal_get(self,question_code):
		question = MKActivityQuestion.get_by_id(int(question_code))
		activity = question.activity
		try:
			db.delete(question.possible_answers)
			db.delete(question.answers)
			question.delete()
			self.set_flash('La pregunta ha sido eliminada')
		except:
			self.set_flash('Hubo un problema eliminando la pregunta', flash_type='error')
		self.redirect('/admin/activity/'+str(activity.key().id())+'/listQuestions')


class AddActivityHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
	 
	 	existing_activity = MKActivity.all()
	 	values = {'existing_activity':existing_activity}
		self.render('add_activity', template_values=values)
		#self.base_auth()
		#self.get_internal()
		#user_logout = users.create_logout_url("/eventos/")
		#self.response.out.write("<a href=\"%s\">Logout</a>." %user_logout)

	def internal_post(self):
		
		activity_name = self.request.get('activity_name')
		
		existing_activity = MKActivity.all().filter('name = ',activity_name).get()
		
		if existing_activity:
			flash_message = 'La activity ya existe'
			values = { 'flash' : flash_message, 'flash_type' : 'error'}
			self.render('add_activity',template_values=values)
			return 
		
		activity = MKActivity()
		activity.name = activity_name
		activity.default_general_feedback = self.request.get('default_general_feedback')
		activity.default_correct_feedback  = self.request.get('default_correct_feedback')
		activity.default_wrong_feedback  = self.request.get('default_wrong_feedback')
		activity.put()
		values = { 
				'activity_code' : str(activity.key().id())
				}
		self.set_flash('Nueva activity '+ activity.name + ' ha sido creada. Por favor, agregale preguntas.')
		self.redirect('/admin/activity/'+str(activity.key().id())+'/addQuestion')
		


def main():
  application = webapp.WSGIApplication([('/admin/activity/questions/(\d*?)/remove', RemoveQuestionHandler),
  										('/admin/activity/(\d*?)/addQuestion', AddQuestionHandler),
										('/admin/activity/add',AddActivityHandler),
										('/admin/activity/(\d*?)/listQuestions',ListActivityQuestionsHandler),
										('/admin/activity/',ListActivityHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
