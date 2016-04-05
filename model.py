from google.appengine.ext import db

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
