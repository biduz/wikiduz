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
	content = db.TextProperty()
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

def new_page(page, author, content):
	new = Pages()
	new.page = page
	new.author = author
	new.content = content
	new.created = datetime.datetime.now()
	new.put()
	import time
	time.sleep(0.5) # TBD: implement a strong consistency using
					# parents/ancestor from GAE Datastore  

def get_page(page):
	return Pages.all().filter('page = ', page).get()
