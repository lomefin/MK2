#!/usr/bin/env python
# coding=UTF-8
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
			
		food.name = unicode(name, 'utf8')
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

		print 'internal_post'
		print self.request.get('foods')
		foods = str(self.request.get('foods')).strip()
		food_lines = foods.split(';')
		for line in food_lines:
			print line
		if MKFoodLogElement.all().count() > 0:
			self.redirect('/admin/foods/list')
			return

		

		self.redirect('/admin/foods/list')

	def internal_get(self):

		self.addfood('Aceite','cucharada',0,0,5,6)
		self.addfood('Acelga','taza',4,2,1,2)
		self.addfood('Achicoria','taza',2,1,0,2)
		self.addfood('Albóndiga','unidad',8,15,7,5)
		self.addfood('Alcachofa','unidad',10,1,0,2)
		self.addfood('Alcachofa mayo','unidad',14,3,13,1)
		self.addfood('Alcachofa vinagreta','unidad',5,1,0,1)
		self.addfood('Alcayota','cucharada',11,0,0,7)
		self.addfood('Almejas','tarro',3,15,1,6)
		self.addfood('Apio','taza',4,1,0,2)
		self.addfood('Arroz','taza',42,4,0,1)
		self.addfood('Arroz con Leche','pote',46,7,6,1)
		self.addfood('Arroz graneado','taza',64,5,11,1)
		self.addfood('Arveja','taza',14,4,0,2)
		self.addfood('Atún en aceite','tarro',1,26,27,5)
		self.addfood('Avena','cucharada',12,2,1,1)
		self.addfood('Azúcar','cucharadita',5,0,0,7)
		self.addfood('Bebida Gaseosa','vaso',22,0,0,7)
		self.addfood('Berenjena','taza',5,1,0,2)
		self.addfood('Berlin','unidad',15,9,71,7)
		self.addfood('Beterraga','taza',7,2,0,2)
		self.addfood('Biscocho Relleno','unidad',63,4,20,7)
		self.addfood('Bistec Alemán','unidad',2,24,6,5)
		self.addfood('Bistec a la plancha','unidad',4,32,5,5)
		self.addfood('Bistec a lo Pobre','plato',58,58,46,5)
		self.addfood('Bistec en aceite','unidad',4,32,10,5)
		self.addfood('Brazo de Reina','plato',13,10,7,5)
		self.addfood('Brocoli','taza',5,3,0,2)
		self.addfood('Budín de verduras','plato',24,7,14,1)
		self.addfood('Caldillo de Pescado','plato',30,35,12,1)
		self.addfood('Carbonada con carne','plato',66,14,16,1)
		self.addfood('Carbonada de verdura','plato',43,7,5,1)
		self.addfood('Carne Vegetal','plato',0,55,1,5)
		self.addfood('Carne al jugo','presa',8,32,10,5)
		self.addfood('Carne asada','unidad',5,43,11,5)
		self.addfood('Carne de Cerdo','trozo',0,25,21,5)
		self.addfood('Carne de Cerdo','trozo',0,25,21,5)
		self.addfood('Carne de Cordero','trozo',0,26,17,5)
		self.addfood('Carne de Vacuno','trozo',0,24,6,5)
		self.addfood('Cazuela Ave','plato',43,20,14,1)
		self.addfood('Cazuela Cerdo','plato',56,26,14,1)
		self.addfood('Cazuela Cordero','plato',53,32,11,1)
		self.addfood('Cazuela Vacuno','plato',56,37,9,1)
		self.addfood('Cazuela albóndiga','plato',47,15,8,1)
		self.addfood('Cebolla','taza',6,1,0,2)
		self.addfood('Cereza','taza',14,2,1,2)
		self.addfood('Champiñones','taza',7,3,1,2)
		self.addfood('Charquicán','plato',55,3,7,1)
		self.addfood('Chirimoya','unidad',12,3,1,3)
		self.addfood('Choclo','unidad',23,5,1,2)
		self.addfood('Cholgas en aceite','tarro',2,26,5,5)
		self.addfood('Choritos en aceite','tarro',2,19,4,5)
		self.addfood('Chuletas de cerdo','unidad',2,27,29,1)
		self.addfood('Ciruela','unidad',10,1,0,3)
		self.addfood('Cochayuyo','taza',9,1,0,2)
		self.addfood('Coliflor','taza',4,2,1,2)
		self.addfood('Compota Ciruela con Mote','pote',58,3,0,1)
		self.addfood('Compota de Fruta','pote',20,1,1,1)
		self.addfood('Compota de Huesillo con Mote','pote',55,2,0,1)
		self.addfood('Conejo Asado','unidad',0,19,2,1)
		self.addfood('Congrio al Vapor','unidad',5,23,0,1)
		self.addfood('Congrio frito','unidad',11,32,32,1)
		self.addfood('Corvina al Vapor','unidad',4,31,1,1)
		self.addfood('Costillas Asadas','plato',0,23,12,1)
		self.addfood('Damasco','unidad',15,1,1,3)
		self.addfood('Dulce Chileno','unidad',20,2,14,1)
		self.addfood('Dulce de Membrillo','tajada',18,0,0,7)
		self.addfood('Durazno o melocotón','unidad',14,1,0,3)
		self.addfood('Empanada Horno','unidad',50,14,16,1)
		self.addfood('Empanada de Pino','unidad',50,12,17,1)
		self.addfood('Empanada frita pino','unidad',33,11,19,1)
		self.addfood('Empanada frita queso','unidad',32,13,15,1)
		self.addfood('Ensalada Rusa','plato',33,8,16,1)
		self.addfood('Ensalada de Cebolla','plato',31,11,1,1)
		self.addfood('Ensalada porotos con cebolla','plato',31,11,1,1)
		self.addfood('Escalopa de vacuno','unidad',18,24,15,1)
		self.addfood('Espinaca','taza',2,2,0,2)
		self.addfood('Espárragos','unidad',2,1,0,2)
		self.addfood('Espárragos limoneta','plato',4,4,16,1)
		self.addfood('Estofado de ave','plato',15,20,16,1)
		self.addfood('Estofado de cordero','plato',15,15,13,1)
		self.addfood('Fiambre en general','tajada',1,5,6,1)
		self.addfood('Fideos','taza',26,5,1,1)
		self.addfood('Flan','unidad',27,4,3,7)
		self.addfood('Flan de Leche','pote',40,8,60,1)
		self.addfood('Flan de verdura','cucharada',0,9,0,1)
		self.addfood('Fritos de verdura','unidad',0,8,0,1)
		self.addfood('Frutillas con azúcar','cucharada',28,1,1,7)
		self.addfood('Frutillas con crema','pote',28,1,6,3)
		self.addfood('Galletas Tritón','unidad',4,0,1,7)
		self.addfood('Galletas de Soda','unidad',4,1,1,1)
		self.addfood('Galletas de Vino','unidad',4,0,1,7)
		self.addfood('Garbanzos','taza',32,10,3,1)
		self.addfood('Garbanzos cocidos','taza',38,13,4,1)
		self.addfood('Garbanzos con tocino','plato',51,19,22,1)
		self.addfood('Goulach','plato',31,24,14,1)
		self.addfood('Guatitas','unidad',0,10,3,5)
		self.addfood('Guatitas','plato',0,24,3,5)
		self.addfood('Haba','taza',3,2,1,2)
		self.addfood('Habas','taza',14,7,1,2)
		self.addfood('Hallulla','unidad',62,8,4,1)
		self.addfood('Hamburguesas','unidad',5,22,15,5)
		self.addfood('Harina tostada con leche','pote',49,10,6,1)
		self.addfood('Helados','unidad',14,1,3,7)
		self.addfood('Higado','trozo',3,24,5,5)
		self.addfood('Huevo','unidad',2,7,5,5)
		self.addfood('Huevo a la copa o duro','unidad',2,7,5,5)
		self.addfood('Huevo con fiambre','unidad',2,8,10,5)
		self.addfood('Huevo con queso','unidad',5,9,9,1)
		self.addfood('Huevo con tocino','unidad',2,7,10,1)
		self.addfood('Huevo frito o revuelto','unidad',2,7,8,5)
		self.addfood('Humita','unidad',43,9,16,1)
		self.addfood('Hígado bistec','unidad',7,30,12,5)
		self.addfood('Jalea con fruta','pote',33,3,0,7)
		self.addfood('Jalea con leche','pote',25,6,6,7)
		self.addfood('Jamón','tajada',0,6,8,5)
		self.addfood('Jamón con palta y lechuga','unidad',5,12,20,1)
		self.addfood('Jamón con papas mayo','plato',41,8,18,1)
		self.addfood('Jamón de pollo','tajada',0,15,4,5)
		self.addfood('Jugo','vaso',3,0,0,7)
		self.addfood('Jurel al vapor','plato',1,32,60,5)
		self.addfood('Jurel en aceite','tarro',1,26,25,5)
		self.addfood('Kiwi','unidad',16,1,1,3)
		self.addfood('Kuchen','unidad',34,3,9,7)
		self.addfood('Lasaña','plato',36,22,15,1)
		self.addfood('Leche Asada','unidad',26,8,3,7)
		self.addfood('Leche Semidescremada','vaso',10,6,3,4)
		self.addfood('Leche asada','pote',33,3,0,7)
		self.addfood('Leche con milo','vaso',28,8,6,4)
		self.addfood('Leche con plátano','cucharada',31,8,6,4)
		self.addfood('Leche condensada','cucharada',12,2,1,7)
		self.addfood('Leche descremada','vaso',10,7,0,4)
		self.addfood('Leche entera','vaso',9,6,7,4)
		self.addfood('Leche nevada','pote',33,8,7,7)
		self.addfood('Lechuga','taza',1,1,0,2)
		self.addfood('Lentejas','taza',37,11,1,1)
		self.addfood('Lentejas con arroz','plato',55,20,11,1)
		self.addfood('Limonada','vaso',15,0,0,1)
		self.addfood('Locos','tarro',6,22,1,5)
		self.addfood('Locos mayo','plato',6,19,29,5)
		self.addfood('Lomo asado','trozo',1,46,16,5)
		self.addfood('Longaniza','unidad',4,8,23,5)
		self.addfood('Lúcuma','unidad',31,1,1,3)
		self.addfood('Macedonia','pote',35,1,1,3)
		self.addfood('Machas','tarro',3,26,3,5)
		self.addfood('Manjar','cucharada',11,2,1,7)
		self.addfood('Mantequilla','cucharada',0,0,5,6)
		self.addfood('Manzana','unidad',17,0,0,3)
		self.addfood('Manzana asada','pote',0,1,0,3)
		self.addfood('Margarina','cucharada',0,0,5,6)
		self.addfood('Margarina Diet','cucharada',0,0,4,6)
		self.addfood('Mariscos en salsa verde','plato',15,20,7,5)
		self.addfood('Marraqueta','unidad',60,6,1,1)
		self.addfood('Mayonesa','cucharada',2,0,2,6)
		self.addfood('Melocotón','unidad',14,1,0,3)
		self.addfood('Melón','tajada',13,1,0,3)
		self.addfood('Membrillo','unidad',13,0,0,3)
		self.addfood('Merengue con azúcar','pote',6,1,0,7)
		self.addfood('Merengue con fruta','pote',30,2,0,7)
		self.addfood('Merluza','cucharada',0,13,1,5)
		self.addfood('Mermelada de Alcayota','cucharada',11,0,0,7)
		self.addfood('Mermelada de Ciruela','cucharada',9,0,0,7)
		self.addfood('Mermelada de Damasco','cucharada',9,0,0,7)
		self.addfood('Mermelada de Durazno','cucharada',10,0,0,7)
		self.addfood('Mermelada de Frutilla','cucharada',12,0,0,7)
		self.addfood('Mermelada de Guinda','cucharada',13,0,0,7)
		self.addfood('Mermelada de Mora','cucharada',9,0,0,7)
		self.addfood('Mermelada de Rosa Mosqueta','cucharada',13,0,0,7)
		self.addfood('Miel de Abeja','cucharadita',5,0,0,7)
		self.addfood('Miniestrón','plato',53,14,4,1)
		self.addfood('Mortadela','tajada',1,4,5,5)
		self.addfood('Naranja','unidad',11,1,0,3)
		self.addfood('Palomitas de maíz','taza',25,5,3,1)
		self.addfood('Palta','unidad',2,0,6,6)
		self.addfood('Palta Rellena','unidad',5,7,30,6)
		self.addfood('Pan Amasado','unidad',37,5,7,1)
		self.addfood('Pan con fiambre','unidad',63,14,11,1)
		self.addfood('Pan con fiambre y mantequilla','unidad',63,14,29,1)
		self.addfood('Pan con manjar','unidad',85,11,6,1)
		self.addfood('Pan con mermelada','unidad',79,8,4,1)
		self.addfood('Pan con paté','unidad',62,11,17,1)
		self.addfood('Pan con queso','unidad',63,18,14,1)
		self.addfood('Pan con queso y mantequilla','unidad',64,18,31,1)
		self.addfood('Pan de Molde','rebanada',16,3,1,1)
		self.addfood('Panqueques','unidad',30,3,4,1)
		self.addfood('Pantrucas','plato',60,10,7,1)
		self.addfood('Papa duquesa','unidad',6,2,2,1)
		self.addfood('Papas','taza',20,2,0,1)
		self.addfood('Papas fritas','plato',76,9,10,1)
		self.addfood('Papas rellenas','unidad',48,19,14,1)
		self.addfood('Papaya','unidad',4,1,0,3)
		self.addfood('Papayas al Jugo','vaso',9,0,0,3)
		self.addfood('Pastel','unidad',75,2,6,1)
		self.addfood('Pastel de Choclo','plato',61,22,27,1)
		self.addfood('Pastel de carne','trozo',21,11,16,1)
		self.addfood('Pastel de mil hojas','unidad',72,4,14,1)
		self.addfood('Pastel de papas','unidad',51,22,15,1)
		self.addfood('Pavo','trozo',1,22,3,5)
		self.addfood('Pavo asado','trozo',1,24,4,5)
		self.addfood('Pepino','taza',2,1,0,2)
		self.addfood('Pepino dulce','unidad',8,1,0,3)
		self.addfood('Pera','unidad',15,0,1,3)
		self.addfood('Pera al jugo','tarro',103,1,1,3)
		self.addfood('Pera compota','pote',10,0,0,1)
		self.addfood('Pernil','trozo',0,33,11,5)
		self.addfood('Pescado','trozo',1,19,7,5)
		self.addfood('Pescado ahumado','trozo',0,26,1,5)
		self.addfood('Pescado al Jugo','trozo',4,31,6,5)
		self.addfood('Pescado al curry','trozo',7,35,8,5)
		self.addfood('Pescado al vapor','trozo',1,26,1,5)
		self.addfood('Pichanga','plato',13,12,14,5)
		self.addfood('Pie de limón','unidad',15,5,47,7)
		self.addfood('Pie de limón','unidad',45,4,12,7)
		self.addfood('Pino de carne','plato',3,16,12,5)
		self.addfood('Pizza','tajada',25,14,9,1)
		self.addfood('Piña al Jugo','tarro',79,2,1,3)
		self.addfood('Plátano','unidad',21,1,0,3)
		self.addfood('Pollo','presa',0,27,7,5)
		self.addfood('Pollo al curry','presa',7,20,10,5)
		self.addfood('Pollo al jugo','presa',6,24,16,5)
		self.addfood('Pollo asado con mantequilla','presa',6,23,16,5)
		self.addfood('Pollo frito apanado','presa',8,2,9,5)
		self.addfood('Poroto granado','taza',4,2,0,2)
		self.addfood('Porotos','taza',31,12,1,1)
		self.addfood('Porotos Verdes','taza',11,3,0,2)
		self.addfood('Porotos cocidos','taza',37,14,186,1)
		self.addfood('Porotos con tallarines','plato',62,20,13,1)
		self.addfood('Porotos granados','plato',63,4,6,1)
		self.addfood('Porotos granados cocidos','taza',31,2,0,1)
		self.addfood('Porotos verdes cocidos','taza',3,1,0,1)
		self.addfood('Prietas','unidad',1,11,9,5)
		self.addfood('Prueba','cucharada',100,100,100,1)
		self.addfood('Puré de papas','plato',56,13,12,1)
		self.addfood('Quaker con leche','pote',44,9,6,1)
		self.addfood('Quesillo','tajada',1,3,1,4)
		self.addfood('Queso','tajada',1,10,11,6)
		self.addfood('Reinteta','trozo',1,19,3,5)
		self.addfood('Repollo','taza',3,1,0,2)
		self.addfood('Roastbeef','trozo',0,28,15,5)
		self.addfood('Salame','tajada',0,3,6,5)
		self.addfood('Salpicón','taza',6,15,16,5)
		self.addfood('Salsa Blanca','cucharada',1,1,2,1)
		self.addfood('Salsa de Tomates','cucharada',4,1,0,6)
		self.addfood('Sandía','tajada',5,0,0,3)
		self.addfood('Sopa con verdura y arroz','plato',24,2,4,1)
		self.addfood('Sopa de mariscos','plato',19,13,3,5)
		self.addfood('Sopa deshidratada','plato',11,2,1,1)
		self.addfood('Sopa menudencias','plato',27,6,60,1)
		self.addfood('Sopaipilla','unidad',8,1,10,1)
		self.addfood('Sopaipilla pasada','unidad',14,1,10,1)
		self.addfood('Strudel de Manzana','unidad',49,4,14,7)
		self.addfood('Surtido para caldillo','tarro',11,35,2,5)
		self.addfood('Sémola con leche','pote',49,8,6,1)
		self.addfood('Tallarines cocidos','taza',52,9,0,1)
		self.addfood('Tallarines con salsa de carne','taza',69,38,10,1)
		self.addfood('Tocino','tajada',0,0,9,6)
		self.addfood('Tomate','unidad',3,1,0,2)
		self.addfood('Tomate relleno','unidad',10,6,10,2)
		self.addfood('Tortilla de verduras','trozo',47,1,0,2)
		self.addfood('Turín','rebanada',1,4,6,7)
		self.addfood('Tuti fruti en conserva','pote',47,1,0,3)
		self.addfood('Uva','unidad',1,0,0,3)
		self.addfood('Vienesa','unidad',0,4,10,5)
		self.addfood('Vienesas','unidad',1,8,18,5)
		self.addfood('Yogurt diet','unidad',10,5,2,4)
		self.addfood('Yougurt','unidad',8,6,6,4)
		self.addfood('Zanahoria','taza',11,1,0,2)
		self.addfood('Zapallo','trozo',6,0,1,2)
		self.addfood('Zapallo Italiano','unidad',6,1,1,2)
				

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
										('/admin/foods/init',InitFoodHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
