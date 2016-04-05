from google.appengine.ext import db
import datetime
import stuff

class Users(db.Model):
	name = db.StringProperty()
	email = db.StringProperty()
	password = db.StringProperty()
	time = db.DateTimeProperty()
	
class Pages(db.Model):
	name = db.StringProperty()
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
	return user.key().id()

def get_user_by_name(username):
	return Users.all().filter('name = ', username).get()

def valid_password(pw, user_id):
	h = Users.get_by_id(user_id).password
	return stuff.valid_pw(pw, h)