import model.models
from model.properties import GenderProperty
from model.properties import WeekModeProperty
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import datastore_errors
from google.appengine.ext.webapp import template
 
class MKModel(db.Model):
	creation_date = db.DateTimeProperty(auto_now_add=True) 
	is_active = db.BooleanProperty(default=True)
	
class MKAvatar(db.Model):
	name = db.StringProperty()
	sex  = GenderProperty()
	prefix = db.StringProperty()
	
class MKAccount(MKModel):
	system_login = db.StringProperty()
	system_password = db.StringProperty()
	g_id = db.StringProperty()
	email = db.EmailProperty()
	name = db.StringProperty()
	surname = db.StringProperty()
	
	last_entrance = db.DateTimeProperty()
	active = db.BooleanProperty()
	wants_email = db.BooleanProperty()
	is_administrator	= db.BooleanProperty()

class MKSchool(MKModel):
	name	  = db.StringProperty()
	administrators = db.ReferenceProperty(MKAccount,collection_name='administrator_list')
	supervised = db.BooleanProperty()

class MKTeacher(MKModel):
	user					= db.ReferenceProperty(MKAccount)
	school					= db.ReferenceProperty(MKSchool,collection_name='school_teachers')
	
class MKClass(MKModel):
	name      = db.StringProperty()
	year      = db.IntegerProperty()
	#students  = db.ReferenceProperty(MKAccount,collection_name='student_list')
	teacher   = db.ReferenceProperty(MKTeacher,collection_name='classes_list')
	school    = db.ReferenceProperty(MKSchool,collection_name='school_classes')	

class MKWeek(db.Model):
	year = db.IntegerProperty()
	number = db.IntegerProperty()
	start_date = db.DateTimeProperty()
	end_date = db.DateTimeProperty()
	school = db.ReferenceProperty(MKSchool,collection_name='school_weeks')
	trivia = db.BooleanProperty()
	food_log = db.BooleanProperty()
	todo = db.BooleanProperty()
	week_mode = WeekModeProperty()
	
class MKStudent(MKModel):
	student_account				= db.ReferenceProperty(MKAccount)
	adult_people_in_house 		= db.IntegerProperty()
	non_adults_in_house 		= db.IntegerProperty()
	student_height				= db.FloatProperty()
	student_weight 				= db.FloatProperty()
	student_gender 				= GenderProperty()
	student_nutritional_status	= db.StringProperty(default=None)
	student_birth_date 			= db.DateTimeProperty()
	student_avatar 				= db.ReferenceProperty(MKAvatar,collection_name='avatar_users')
	attending_class				= db.ReferenceProperty(MKClass,collection_name='class_students')
	has_started 				= db.BooleanProperty()

class MKTrivia(MKModel):
	name		= db.StringProperty()
	default_general_feedback = db.StringProperty()
	default_correct_feedback  = db.StringProperty()
	default_wrong_feedback  = db.StringProperty()
	
class MKTriviaQuestion(MKModel):
	created_by = db.ReferenceProperty(MKAccount)
	trivia = db.ReferenceProperty(MKTrivia,collection_name='questions')
	question_text = db.StringProperty()
	general_feedback = db.StringProperty()
	phrase = db.StringProperty()
	last_displayed = db.DateTimeProperty()

class MKTriviaPossibleAnswer(MKModel):
	possible_answer_text = db.StringProperty()
	feedback_text = db.StringProperty()
	is_correct = db.BooleanProperty()
	question = db.ReferenceProperty(MKTriviaQuestion,collection_name='possible_answers')
	
class MKTriviaAnswer(MKModel):
	answered_by = db.ReferenceProperty(MKStudent,collection_name="trivia_answers")
	question = db.ReferenceProperty(MKTriviaQuestion, collection_name="answers")
	answered = db.ReferenceProperty(MKTriviaPossibleAnswer, collection_name="responses")
	
class MKFoodLogElement(MKModel):
	created_by = db.ReferenceProperty(MKAccount)
	group = db.IntegerProperty()
	name = db.StringProperty()
	protein_calories = db.IntegerProperty()
	fat_calories = db.IntegerProperty()
	carb_calories = db.IntegerProperty()
	serves_snack = db.BooleanProperty()
	serves_dinner = db.BooleanProperty()
	serves_lunch = db.BooleanProperty()
	serves_breakfast = db.BooleanProperty()
	unit = db.StringProperty()
	
class MKDailyFoodLog(MKModel):
	total_fats = db.IntegerProperty()
	total_proteins = db.IntegerProperty()
	total_carbs = db.IntegerProperty()
	total_calories = db.IntegerProperty()
	created_by = db.ReferenceProperty(MKAccount, collection_name='food_logs')
	

class MKFoodLogElementConsumption(MKModel):
	consumed = db.ReferenceProperty(MKFoodLogElement,collection_name='food_consumers')
	consumed_by = db.ReferenceProperty(MKAccount,collection_name='food_consumptions')
	reported_in = db.ReferenceProperty(MKDailyFoodLog,collection_name='reporte_consumptions')
	amount = db.IntegerProperty()

class MKFoodLogAnswer(MKModel):
	answered_by = db.ReferenceProperty(MKAccount)
	consumptions = db.ReferenceProperty(MKFoodLogElementConsumption,collection_name='consumption_list')
	
class MKGoal(MKModel):
	created_by = db.ReferenceProperty(MKAccount,collection_name="goals")
	goal = db.StringProperty()
	date_completed = db.DateTimeProperty()
	
class MKLink(MKModel):
	created_by = db.ReferenceProperty(MKAccount)
	name = db.StringProperty()
	link = db.StringProperty()
	
class MKMissingFood(MKModel):
	created_by 	= db.ReferenceProperty(MKAccount)
	text		= db.StringProperty()
	
class MKContactData(MKModel):
	created_by = db.ReferenceProperty(MKAccount)
	status     = db.StringProperty()
	resolved   = db.BooleanProperty()
	module	   = db.StringProperty()
	activity   = db.StringProperty()
	details    = db.TextProperty()
	url	   = db.StringProperty()
	solution   = db.StringProperty()
class MKNews(MKModel):
	message = db.StringProperty(multiline=True)
class MKAccess(MKModel):
	student = db.ReferenceProperty(MKStudent,collection_name="accesses")
class MKMooreResult(MKModel):
	student = db.ReferenceProperty(MKStudent,collection_name="moore_results")
	seen = db.BooleanProperty(default=False)
	item42 = db.IntegerProperty(default=0)
	item12 = db.IntegerProperty(default=0)
	item13 = db.IntegerProperty(default=0)
	item17 = db.IntegerProperty(default=0)

class MKWelcomeMessage(MKModel):
	title = db.StringProperty()
	body = db.TextProperty()

class MKConfig(MKModel):
	name = db.StringProperty()
	value = db.StringProperty()