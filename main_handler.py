import webapp2
import jinja2
import session
import stuff
import model
import logging
import os

class MainHandler(webapp2.RequestHandler):
    def initialize(self,request, response):
        super(MainHandler, self).initialize(request, response)
        self.user = self.is_logged()

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

    def get_cookie(self, cookie):
        return self.request.cookies.get(cookie)

    def delete_user_cookie(self):
        self.set_cookie('user=')

    def login(self, user):
        session.new_session(user)
        self.set_user_cookie(user.key().id())

    def logout(self, user=None):
        if not user:
            self.delete_user_cookie()
        else:
            session.delete_session(user)
            self.delete_user_cookie()

    def is_logged(self):
        user_cookie = self.get_cookie('user')
        try:
            if user_cookie and stuff.check_secure_val(user_cookie):
                user_id = stuff.get_val_from_secure_val(user_cookie)
                return model.get_user_by_id(int(user_id))
        except ValueError, e:
            logging.error('Error checking if is logged\n ValueError: %s' % e)
            return
