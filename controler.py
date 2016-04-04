import webapp2
import jinja2
import os

class MainHandler(webapp2.RequestHandler):
	def write(self, response):
		self.response.write(response)

	def render(self, template, **params):
		template_dir = os.path.join(os.path.dirname(__file__), 'templates')
		env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
		template = env.get_template(template)
		self.write(template.render(params))

class Index(MainHandler):
	def get(self):
		self.render('index.html')

class Signup(MainHandler):
	def get(self):
		self.render('signup.html')

	def post(self):
		pass

class Login(MainHandler):
	def get(self):
		self.render('login.html')

	def post(self):
		pass

class Edit(MainHandler):
	def get(self, page):
		self.render('edit.html')

	def post(self, page):
		pass
		
class Logout(MainHandler):
	def get(self):
		pass

class WikiPage(MainHandler):
	def get(self, page):
		pass

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/', Index),
							   ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/_edit' + PAGE_RE, Edit),
                               (PAGE_RE, WikiPage)
							    ], 
							     debug = True)