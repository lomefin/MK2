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
from lib.calorie_analysis  import  *
from model.models import *

class FoodTime:
	pass

class FoodLogIndexHandler(mkhandler.MKHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def internal_get(self):
		
		food_items = MKFoodLogElement.all().order('name')
		
		
		
		kid_data = ''
		if self.current_student_user and self.current_student_user.student_avatar:
		 	kid_data = self.current_student_user.student_avatar.sex + "-" + self.current_student_user.student_avatar.prefix + "-normal"
		values = { 'food_items' : food_items , 'kid_data' : kid_data , 'show_kid': True} 
		self.render('index',template_values=values)
		#self.base_auth()
		#self.get_internal()
		#user_logout = users.create_logout_url("/eventos/")
		#self.response.out.write("<a href=\"%s\">Logout</a>." %user_logout)
		
	def internal_post(self):
		food_log = MKDailyFoodLog()
		food_log.created_by = self.current_student_user.student_account
		food_log.put()
		arguments = self.request.arguments()
		total_carbs = 0
		total_proteins = 0
		total_fats = 0
		missing = self.request.get('missing_food')
		
		for arg in arguments:
			try:
				food = self.request.get_all(arg)
				
				sum = 0	
				for i in food:
					sum = sum + int(i)
				if(sum == 0):
					continue
				food = MKFoodLogElement.get_by_id(int(arg))
				total_proteins = total_proteins + food.protein_calories * sum * 9
				total_fats = total_fats + food.fat_calories * sum * 4
				total_carbs = total_carbs + food.carb_calories * sum * 4
				consumption = MKFoodLogElementConsumption()
				consumption.consumed = food
				consumption.consumed_by = self.current_student_user.student_account
				consumption.amount = sum
				consumption.reported_in = food_log
				consumption.put()
			except:
				pass
		
		food_log.total_proteins = total_proteins
		food_log.total_fats = total_fats
		food_log.total_carbs = total_carbs
		food_log.total_calories = total_proteins + total_fats+ total_carbs
		if food_log.total_calories == 0:
			self.redirect('/food_log/')
			return
		food_log.put()
		
		if(missing and len(missing) > 0):
			missing_food = MKMissingFood()
			missing_food.created_by = self.current_student_user.student_account
			missing_food.text = missing
			missing_food.put()
		
		values = { 'flash' :  arguments} 
		self.redirect('showResults/'+str(food_log.key().id()))
		
		
class FoodLogResultHandler(mkhandler.MKHandler):

	def base_directory(self):
		return os.path.dirname(__file__)
	def get(self, log_id):
		self.auth_check()
		self.internal_get(log_id)
		
	def internal_get(self,log_id):
		analizer = CalorieAnalysis()
		student_age = int((datetime.datetime.now() - self.current_student_user.student_birth_date).days/365.25)
		analizer.set_user_data(student_age,self.current_student_user.student_height,self.current_student_user.student_weight,self.current_student_user.student_gender)
		food_log = MKDailyFoodLog.get_by_id(int(log_id))
		
		analizer.set_calories_consumption(food_log.total_proteins,food_log.total_carbs,food_log.total_fats)
		result = analizer.generate_analysis()
		kid_data = ''
		if self.current_student_user and self.current_student_user.student_avatar:
		 	kid_data = self.current_student_user.student_avatar.sex + "-" + self.current_student_user.student_avatar.prefix + "-lean"
		values = { 
			'range02' : [0,1,2],
			'analyzer' : analizer,
			'chart_values':[food_log.total_proteins,food_log.total_fats,food_log.total_carbs,food_log.total_calories],
			'percentages':  [	100*food_log.total_proteins/food_log.total_calories,
		  						100*food_log.total_fats/food_log.total_calories,
		  						100*food_log.total_carbs/food_log.total_calories],
			'kid_data' : kid_data, 
			'show_kid': True, 
			'analysis_result': result,
			'bubble_data' : result['message'],
			'bubble_data_class' : result['message_category'], 
			'bubble_data_image' : result['message_category']
		} 
		self.render('show_results',template_values=values);
		pass
	
	def post(self, log_id):
		pass
		
def main():
  application = webapp.WSGIApplication([('/food_log/showResults/(\d*)',FoodLogResultHandler),('/food_log/.*', FoodLogIndexHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
