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

    def set_cookie(self, cookie):
    	self.response.headers.add_header('Set-Cookie', 'user=%s' % cookie)

    def login(self, user):
    	self.set_cookie(user.key().id())