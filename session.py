import string
import random

session = {}

def new_session(user):
	session[user.key().id()] = {}
	session[user.key().id()]['token'] = make_salt()

def delete_session(user):
	del session[user.key().id()]

def get_session_token(user_id):
	try:
		return session[user_id]['token']
	except:
		return None

def make_salt(n=20):
	chars = string.digits + string.letters
	return ''.join(random.choice(chars) for x in range(n))