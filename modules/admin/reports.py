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
import datetime
from model.models import *
import random
import string			

class ListReportsHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		
		
		
		values = {
		  'report_list':['/admin/reports/pending_food','/admin/reports/foodlog']
		}
		
		self.render('list_report',template_values=values)
	
	def post(self,second_argument):
		self.auth_check()
		self.internal_post(second_argument)
	
	def internal_post(self,class_id):
		
		flash_message = ''

class FoodlogReportHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		classes = MKClass.all().order("name")
		values = { 'classes' : classes }
		self.render('report_foodlog',template_values=values)

	def internal_post(self):
		mkclass = MKClass.get_by_id(int(self.request.get('school_class')))
		classes = MKClass.all().order("name")
		students = mkclass.class_students


		values = {'mkclass':mkclass,'classes':classes,'students':students}

		self.render('report_foodlog',template_values=values)

class GeneralReportHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
		
	def internal_get(self):
	  
		answered_trivia_questions = 0
		accesses = 0
		food_logs = 0
		todos = 0
		todos_done = 0
		query= db.Query(MKTriviaAnswer,keys_only=True)
		while True:
		  count = query.count()
		  answered_trivia_questions = answered_trivia_questions + count
		  if count < 1000:
		    break
		  cursor = query.cursor()
		  query.with_cursor(cursor)
		
		values = {'answered_trivia_questions':answered_trivia_questions}
		
			
		query= db.Query(MKDailyFoodLog,keys_only=True)
		while True:
		  count = query.count()
		  food_logs = food_logs + count
		  if count < 1000:
		    break
		  cursor = query.cursor()
		  query.with_cursor(cursor)
		values['food_logs'] = food_logs
		
		query= db.Query(MKGoal,keys_only=True)
		while True:
		  count = query.count()
		  todos = todos + count
		  if count < 1000:
		    break
		  cursor = query.cursor()
		  query.with_cursor(cursor)
		values['todos'] = todos
		
		query= db.Query(MKGoal,keys_only=True).filter('date_completed > ',0)
		while True:
		  count = query.count()
		  todos_done = todos_done + count
		  if count < 1000:
		    break
		  cursor = query.cursor()
		  query.with_cursor(cursor)
		values['todos_done'] = todos_done
		
		self.render('report_general',template_values=values)

class PendingFoodsHandler(mkhandler.MKGAEHandler):
	def base_directory(self):
		return os.path.dirname(__file__)
		
	def internal_get(self):
	  
		missing_foods = MKMissingFood.all()
		
		values = {'missing_foods':missing_foods}
		
		self.render('report_missing_food',template_values=values)


def main():
  application = webapp.WSGIApplication([('/admin/reports/list', ListReportsHandler),
					('/admin/reports/pending_food',PendingFoodsHandler),
					('/admin/reports/foodlog',FoodlogReportHandler),
					('/admin/reports/general_report',GeneralReportHandler)
										],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
