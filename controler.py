import webapp2
import jinja2
import model
import os
import re

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

def valid_username(username):
    return username and re.match('^[\S]+$', username)

def valid_password(password, verify):
    return password and password == verify

def valid_email(email):
    return not email or re.match('^[\S]+@[\S]+\.[\S]+$', email)

class Signup(MainHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        have_error = False
        params = {'username_value': username,
                  'email_value': email}
        if not valid_username(username):
            have_error = True
            params['username_error'] = "That's not a valid username."
        if not password:
            have_error = True
            params['password_error'] = "That's not a valid password."   
        elif not valid_password(password, verify):
            have_error = True
            params['verify_error'] = "Sorry, the passwords didn't match."
        if not valid_email(email):
            have_error = True
            params['email_error'] = "That's not a valid e-mail."
        
        if have_error:
            self.render('signup.html', **params)       
        else:
            user = model.new_user(username, email, password)
            self.response.headers.add_header('Set-Cookie', 'user=%s' % user)
            self.redirect('/')

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