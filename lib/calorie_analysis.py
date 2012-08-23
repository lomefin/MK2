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
from model.models import *
from model.properties import GenderProperty

class IMCCalculator:
	
	def set_user_data(self,height,weight,gender):
		imc = weight/(height*height/10000)
		self.value = imc
		
		if str(gender) == "masculino":
			if imc < 20:
				self.status = "bajo peso"
			elif imc < 24:
				self.status = "normal"
			elif imc < 29:
				self.status = "riesgo de obesidad"
			else:
				self.status = "obeso"
		else:
			if imc < 19:
				self.status = "bajo peso"
			elif imc < 23:
				self.status = "normal"
			elif imc < 28:
				self.status = "riesgo de obesidad"
			else:
				self.status = "obeso"
				
	def check_imc_of_student(self, student_account):
		try:
			sa = student_account
			self.set_user_data(sa.student_height,sa.student_weight,sa.student_gender)
		except:
			self.status = ""

class CalorieAnalysis:
	
	
	def set_calories_consumption(self,from_proteins,from_carbs,from_fats):
		self.total = from_proteins + from_carbs + from_fats
		self.prot = float(from_proteins) / self.total
		self.carb = float(from_carbs) / self.total
		self.fat = float(from_fats) /self.total
	
	def set_user_data(self,age,height,weight,gender):
		self.age = age
		self.gender = gender
		self.height = height
		self.weight = weight
		self.imc = IMCCalculator()
		self.imc.set_user_data(height,weight,gender)
		
		#Sacado de los apuntes de Salud y Desarrollo del Adolescente , PUC
		if (self.gender == "masculino"):
			#IMC promedio de la poblacion a los 12 años
			self.acceptable_weight_factor = 17.5
			self.minimal_required_calories = (17.5*self.weight + 651) * 1.3
		else:
			self.acceptable_weight_factor = 18
			self.minimal_required_calories = (12*self.weight + 746) * 1.3
		
		self.acceptable_weight = self.acceptable_weight_factor * self.height*self.height/10000
		

	def generate_analysis(self):
	
		#output_message = 'Tu distribucion es de %2.2f\% de proteinas %2.2f\% de grasas y %2.2f\% de carbohidratos para un total de %4.0f'  % (self.prot*100 ,self.fat*100,self.carb*100,self.total)
		
		output_message = str((self.prot*100 ,self.fat*100,self.carb*100,self.total))
		output_message = '¡ Muy bien, la distribucion de nutrientes de tu dieta esta dentro de los rangos normales!'
		message_category = 'ok'
		if (self.prot 	> 0.12 	and self.prot 	< 	0.15 	and
			self.fat 	> 0.2 	and self.fat 	<	0.3 	and
			self.carb	> 0.55	and self.carb 	<	0.68):
			output_message = '¡ Muy bien, la distribucion de nutrientes de tu dieta esta dentro de los rangos normales!'
			message_category = 'ok'
		
		#WARNINGS
		#Muchas proteínas 		pocos carbohidratos
		elif (self.prot 	>= 0.15 	and
			self.fat 	> 0.2 	and self.fat 	<	0.3 	and
			self.carb	<= 0.55):
			output_message =  '¡Bien la distribucion de grasas de tu dieta esta dentro de los rangos normales!... ¡Pero cuidado,  estas consumiendo muchas proteinas y pocos carbohidratos! Recuerda que el exceso de proteínas puede ser perjudicial para tu salud.   Se requiere consumir carbohidratos ya que es la principal fuente de energia de nuestro cuerpo.'
			message_category = 'warning'
		#Muchas proteínas 		pocas grasas
		elif (self.prot 	>=	0.15 	and
			self.fat 	<= 0.2 	and
			self.carb	> 0.55	and self.carb 	<	0.68):
			output_message = '¡Bien la distribucion de carbohidratos de tu dieta esta dentro de los rangos normales!... ¡Pero cuidado,  estas consumiendo muchas proteinas y pocas grasas!  Recuerda que las grasas contienen acidos grasos que son esenciales para muchos pocesos metabólicos de tu organismo y el exceso de proteínas puede ser perjudicial para tu salud.         '
			message_category = 'warning'
		#Muchos carbohidratos pocas proteinas
		elif (self.prot 	<= 0.12	and
			self.fat 	> 0.2 	and self.fat 	<	0.3 	and
			self.carb	>=0.68):
			output_message = '¡Bien la distribucion de grasas de tu dieta esta dentro de los rangos normales!... Pero cuidado,  estas consumiendo pocas proteinas y muchos carbohidratos! Recuerda que las proteínas son esenciales para la mantención y reparacion de tejidos de tu cuerpo y el el exeso de carbohidratos  es perjudicial para tu salud, ya que nuestro organismo los acumula en forma de grasa.'
			message_category = 'warning'
		#Muchos carbohidratos pocas grasas
		elif (self.prot 	<= 0.12 and
			self.fat 	> 0.2 	and self.fat 	<	0.3 	and
			self.carb	>= 0.68):
			output_message = '¡Bien la distribucion de proteínas de tu dieta esta dentro de los rangos normales!... Pero cuidado,  estás consumiendo pocas grasas y muchos carbohidratos! Recuerda que las grasas contienen acidos grasos que son esenciales para muchos pocesos metabólicos de tu organismo y el exeso de carbohidratos  es perjudicial para tu salud, ya que nuestro organismo los acumula en forma de grasa que es perjudicial para tu salud.'
			message_category = 'warning'
		#Muchas grasas Pocas proteínas
		elif (self.prot 	<= 	0.15 	and
			self.fat 	>= 0.3 	and
			self.carb	> 0.55	and self.carb 	<	0.68):
			output_message = '¡Bien la distribucion de carbohidratos de tu dieta esta dentro de los rangos normales!... ¡Pero cuidado,  estas consumiendo muchas proteinas y pocas grasas!  Recuerda que las grasas contienen acidos grasos que son esenciales para muchos pocesos metabólicos de tu organismo y el exceso de proteínas puede ser perjudicial para tu salud.         '
			message_category = 'warning'
		#Muchas grasas pocos carbohidratos
		elif (self.prot 	> 0.12 	and self.prot 	< 	0.15 	and
			self.fat 	>= 0.3 	and
			self.carb	<= 0.55):
			output_message = '¡Bien la distribucion de proteínas de tu dieta esta dentro de los rangos normales!... Pero cuidado,  estas consumiendo muchas grasas y pocos carbohidratos! Recuerda que el exceso de grasas es perjudicial para nuestro organismo. Se requiere consumir carbohidratos ya que es la principal fuente de energia de nuestro cuerpo.    '
			message_category = 'warning'
		
		#PROBLEMAS
		#Muchas proteínas y grasas, y pocos carbohidratos
		elif (self.prot 	>= 	0.15 	and
			self.fat 	>=	0.3 	and
			self.carb	<= 0.55):
			output_message = '¡Cuidado, la distribucion de nutrientes de tu dieta no es la adecuada para tu salud!  Recuerda que el exceso de grasas y carbohidratos es perjudicial para nuestro organismo. '
			message_category = 'not'
		#Muchas proteínas y carbohidratos y pocas grasas
		elif (self.prot 	>= 	0.15 	and
			self.fat 	<= 0.2	and
			self.carb	>=	0.68):
			output_message = '¡Cuidado, la distribucion de nutrientes de tu dieta no es la adecuada para tu salud!  Recuerda que el exceso de proteínas y carbohidratos es perjudicial para nuestro organismo. '
			message_category = 'not'
		#Muchas carbohidratos y grasas y pocas proteínas   
		elif (self.prot 	<= 0.12 	and
			self.fat 	>=	0.3 	and
			self.carb	>=	0.68):
			output_message = '¡Cuidado, la distribucion de nutrientes de tu dieta no es la adecuada para tu salud!  Recuerda que el exceso de grasas y carbohidratos es perjudicial para nuestro organismo.  Recuerda que las proteínas son esenciales para la mantención y reparacion de tejidos de tu cuerpo '
			message_category = 'not'

		analysis = {'message': output_message, 'message_category' : message_category , 'check': 'check'}
		return analysis
		


		