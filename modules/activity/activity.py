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
import string
import datetime
from datetime import date, timedelta
from time import strptime
import logging
from model.models import *

class ActivityIndexHandler(mkhandler.MKHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	
	def next_question(self):
		selected_question = MKActivity.all().get().questions.order('last_displayed').get()
		if not selected_question:
			return None
		selected_question.last_displayed = datetime.datetime.now()
		selected_question.put()
		
		return selected_question
	
	def internal_get(self):

		values = {}
		trivias_answered = 1
		if(self.session and self.session.has_key("ACTIVITIES_ANSWERED")):
			trivias_answered = self.session["ACTIVITIES_ANSWERED"]
		self.session["ACTIVITIES_ANSWERED"] = trivias_answered + 1

		next_question = self.next_question()
		
		flash = ''
		if not next_question:
			try:
				kid_face = self.current_student_user.student_avatar.sex + "-" + self.current_student_user.student_avatar.prefix + "-ok"
				values = { 'kid_face': kid_face}
			except:
				pass
			self.render('notrivia', template_values=values)
			return
		
		values = { 'flash' : flash , 'question' : next_question}
		
		self.render('index', template_values=values)
		

class ActivityAnswerHandler(mkhandler.MKHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_post(self):
		
		question_code = self.request.get('triviaQuestion')
		answer_code = self.request.get('triviaAnswer')
		answer = MKActivityAnswer()
		question = MKActivityQuestion.get_by_id(int(question_code))
		question_answer = MKActivityPossibleAnswer.get_by_id(int(answer_code))
		answer.answered_by = self.current_student_user
		answer.question = question
		answer.answered = question_answer
		answer.put()
		
		#result_icon = 'ok'
		
		feedback = "No le acertaste!"
		result_feedBack = ""
		if(question_answer.is_correct):
			result_icon = 'ok'
			result_feedback = 'Correcta'
			feedback = "Correcto!"
		else:
			result_feedback = 'Incorrecta'
		if(question_answer.feedback_text):
			result_feedback = question_answer.feedback_text
		
		if(question.general_feedback):
			feedback = question.general_feedback
				
			
		kid_data = ''
		kid_face = ''
		if self.current_student_user.student_avatar:
		 	kid_data = self.current_student_user.student_avatar.sex + "-" + self.current_student_user.student_avatar.prefix + "-stand"
			if(question_answer.is_correct):
				kid_face = self.current_student_user.student_avatar.sex + "-" + self.current_student_user.student_avatar.prefix + "-ok"
		values = { 'bubble_data' : 	question.phrase,'feedback' : feedback, 'result_feedback' : result_feedback,
					'flash' : self.flash , 'answer': answer, 'kid_data' : kid_data, 'kid_face' :kid_face}
		values.update({'question':question})
		self.render('answer', template_values=values)

def main():
  application = webapp.WSGIApplication([('/activity/answer/', ActivityAnswerHandler),
										('/activity/*', ActivityIndexHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
