from google.appengine.ext import db
import datetime
from google.appengine.api import memcache

class Users(db.Model):
	name = db.StringProperty()
	email = db.StringProperty()
	password = db.StringProperty()
	time = db.DateTimeProperty()
	
class Pages(db.Model):
	path = db.StringProperty()
	author = db.StringProperty()
	content = db.TextProperty()
	date = db.DateTimeProperty()

class PageCache():
	def __init__(self, page):
		self.path = page.path
		self.author = page.author
		self.date = page.date
		self.content = page.content

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

def new_page(path, author, content):
	new = Pages()
	new.path = path
	new.author = author
	new.content = content
	date = datetime.datetime.now()
	new.date = date
	new.put()
	# Put equivalent object in memcache to workaround consistency problem
	cache_page = PageCache(new)
	memcache.set(path, cache_page)

def edit_page(path, editor, content):
	edit = Pages()
	edit.path = path
	edit.content = content
	edit.author = editor
	date = datetime.datetime.now()
	edit.date = date
	edit.put()
	# Update the values of the object in memcache
	cache_page = PageCache(edit)
	memcache.set(path, cache_page)

def get_page(path):
	page = memcache.get(path)
	if not page:
		page = get_page_by_path(path).get()
		if not page:
			return
		cache_page = PageCache(page)
		memcache.set(path, cache_page)
		return cache_page
	return page

def get_page_editions(path):
	return list(get_page_by_path(path))

def get_page_by_path(path):
	return Pages.all().filter('path = ', path).order('-date')

def get_page_by_id(page_id):
	return Pages.get_by_id(page_id)
