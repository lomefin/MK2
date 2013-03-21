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

class ListFoodHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	
	
	def internal_get(self):
		
		food_elements = MKFoodLogElement.all().order('name')
		values = {
				'food_elements':food_elements,
				'value1' : 'value1',
				'value2' : 'value2'
				
		}
		self.render('list_food',template_values=values)
		#self.base_auth()
		#self.get_internal()
		#user_logout = users.create_logout_url("/eventos/")
		#self.response.out.write("<a href=\"%s\">Logout</a>." %user_logout)

	
class EditFoodHandler(mkhandler.MKGAEHandler):		
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,food_code):
		self.auth_check()
		self.internal_get(food_code)
		
	def internal_get(self,food_code):
		values = {
			'food':MKFoodLogElement.get_by_id(int(food_code)),
			'range1to7':range(8)
		}
		self.render('edit_food',template_values=values)
		
	def internal_post(self,food_code):
		try:
			food = MKFoodLogElement.get_by_id(int(food_code))
			
			
			food.group 				= int(self.request.get('food_group'))
			
			food.put()
			self.set_flash('Alimento editado')
		except:
			self.set_flash('Hubo un problema editando')
		self.redirect('/admin/foods/list')
		
	def post(self,food_code):
		self.auth_check()
		self.internal_post(food_code)
		
class DeleteFoodHandler(mkhandler.MKGAEHandler):		
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,food_code):
		self.auth_check()
		self.internal_get(food_code)
		
	def internal_get(self,food_code):
		values = {
			'food':MKFoodLogElement.get_by_id(int(food_code)),
			'range1to7':range(8)
		}
		MKFoodLogElement.get_by_id
		self.render('edit_food',template_values=values)
		
	def internal_post(self,food_code):
		try:
			food = MKFoodLogElement.get_by_id(int(food_code))
			
			
			food.group 				= int(self.request.get('food_group'))
			
			food.put()
			self.set_flash('Alimento editado')
		except:
			self.set_flash('Hubo un problema editando')
		self.redirect('/admin/foods/list')
		
	def post(self,food_code):
		self.auth_check()
		self.internal_post(food_code)
		
		
class FoodElementView(mkhandler.MKGAEHandler):		
	def base_directory(self):
		return os.path.dirname(__file__)
	
	def get(self,food_code):
		self.auth_check()
		self.internal_get(food_code)
		
	def internal_get(self,food_code):
		pass
class InitFoodHandler(mkhandler.MKGAEHandler):

	def addfood(self,name,unit,carbs,prots,fats,group):
	
		if group is None:
			group = 0
		food = MKFoodLogElement()
			
		food.name = str(name)
		food.protein_calories = int(prots)
		food.fat_calories = int(fats)
		food.carb_calories = int(carbs)
		try:
			food.group 				= int(group)
		except:
			pass
		food.unit = unit
		
		food.put()

	def base_directory(self):
		return os.path.dirname(__file__)
	def internal_post(self):

		print 'internal_get'
		if MKFoodLogElement.all().count() > 0:
			self.redirect('/admin/foods/list')
			return

		

		self.redirect('/admin/foods/list')

	def internal_get(self):

		self.render('init_food')
		

class AddFoodHandler(mkhandler.MKGAEHandler):
	
	def base_directory(self):
		return os.path.dirname(__file__)
	
	
	def internal_get(self):
		values = {
			'range3' : range(3),
		}
		self.render('add_food',template_values=values)
		#self.base_auth()
		#self.get_internal()
		#user_logout = users.create_logout_url("/eventos/")
		#self.response.out.write("<a href=\"%s\">Logout</a>." %user_logout)

	def internal_post(self):
	
		food_name = self.request.get('name').strip()
		if len(food_name) == 0:
			values = { 'flash' : 'No se ha guardado, no tiene nombre'}
			self.render('add_food',template_values=values);
			return
		food_unit = self.request.get('unit').strip()
		prot_cal  = self.request.get('protein_calories').strip()
		carb_cal  = self.request.get('carb_calories').strip()
		fat_cal   = self.request.get('fat_calories').strip()
		
		if sum == 0:
			values = { 'flash' : 'No se ha guardado, no esta destinado a ninguna comida'}
			self.render('add_food',template_values=values);
			return
		
		
		food = MKFoodLogElement()
		
		food.name = food_name
		food.protein_calories = int(prot_cal)
		food.fat_calories = int(fat_cal)
		food.carb_calories = int(carb_cal)
		try:
			food.group 				= int(self.request.get('food_group'))
		except:
			pass
		food.serves_snack 		= self.request.get('serves_snack') == "true" 
		food.serves_dinner 		= self.request.get('serves_dinner') == "true"
		food.serves_lunch 		= self.request.get('serves_lunch') == "true"
		food.serves_breakfast 	= self.request.get('serves_breakfast') == "true"
		food.unit = food_unit
		
		food.put()
	
		values = { 'flash' : 'Se ha agregado el alimento exitosamente.'}
		self.render('add_food',template_values=values);



def main():
  application = webapp.WSGIApplication([('/admin/foods/add',AddFoodHandler)
										,('/admin/foods/list',ListFoodHandler)
										,('/admin/foods/(\d*)/edit',EditFoodHandler),
										('/admin/food/init',InitFoodHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
