from google.appengine.ext import db
import datetime
import stuff
from google.appengine.api import memcache

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

class PageCache():
	def __init__(self, page):
		self.id = page.key().id()
		self.page = page.page
		self.author = page.author
		self.content = page.content
		self.last_edit_by = page.last_edit_by
		self.last_edit_date = page.last_edit_date
		self.created = page.created

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
	created = datetime.datetime.now()
	new.created = created
	new.put()
	# Put equivalent object in memcache to workaround consistency problem
	cache_page = PageCache(new)
	memcache.set(page, cache_page)

def edit_page(page, editor, content):
	page_obj = get_page(page) # Get PageCache instance
	edit = get_page_by_id(page_obj.id)
	edit.content = content
	edit.last_edit_by = editor
	date = datetime.datetime.now()
	edit.last_edit_date = date
	edit.put()
	# Update the values of the object in memcache
	page_obj.content = content
	page_obj.last_edit_by = editor
	page_obj.last_edit_date = date
	memcache.set(page, page_obj)

def get_page(path):
	page = memcache.get(path)
	if not page:
		page = get_page_by_path(path)
		if not page:
			return
		cache_page = PageCache(page)
		memcache.set(path, cache_page)
		return cache_page
	return page

def get_page_by_path(path):
	return Pages.all().filter('page = ', path).get()

def get_page_by_id(page_id):
	return Pages.get_by_id(page_id)
