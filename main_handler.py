import webapp2
import jinja2
import session
import stuff
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
    	self.response.headers.add_header('Set-Cookie', '%s; Path=/' % cookie)

    def set_user_cookie(self, user_id):
        user_cookie = stuff.make_user_cookie(user_id)
        self.set_cookie('user=%s' % user_cookie)

    def login(self, user):
    	session.new_session(user)
        self.set_user_cookie(user.key().id())