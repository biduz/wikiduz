from google.appengine.ext import db
import datetime
import stuff

class Users(db.Model):
	name = db.StringProperty()
	email = db.StringProperty()
	password = db.StringProperty()
	time = db.DateTimeProperty()
	
class Pages(db.Model):
	page = db.StringProperty()
	author = db.StringProperty()
	last_edit_by = db.StringProperty()
	last_edit_date = db.DateTimeProperty()
	created = db.DateTimeProperty()

def new_user(name, email, password):
	user = Users()
	user.name = name
	user.email = email
	user.password = password
	user.time = datetime.datetime.now()
	user.put()
	return user

def get_user_by_name(username):
	return Users.all().filter('name = ', username).get()

def get_user_by_id(user_id):
	return Users.get_by_id(user_id)

def new_page(page, author):
	new_page = Pages()
	new_page.page = page
	new_page.author = author
	new_page.created = datetime.datetime.now()
	new_page.put() 
