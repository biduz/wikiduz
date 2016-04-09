from main_handler import MainHandler
import model
import stuff
import re

class Index(MainHandler):
    def get(self):
        self.render('index.html')

def available_username(username):
    return not model.get_user_by_name(username)

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
        elif not available_username(username):
            have_error = True
            params['username_error'] = "That username is not available"
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
            password = stuff.make_pw_hash(password)
            user = model.new_user(username, email, password)
            self.login(user)
            self.redirect('/')

class Login(MainHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        user = model.get_user_by_name(username)
        if user:
            if stuff.valid_pw(password, user.password):
                self.login(user)
                self.redirect('/')
            else:
                error = 'Invalid Password'
                self.render('login.html', username = username, error = error)    
        else:
            error = 'Invalid User'
            self.render('login.html', username = username, error = error)

class Logout(MainHandler):
    def get(self):
        try:
            user_cookie = self.get_cookie('user')
            user_id = int(stuff.get_val_from_secure_val(user_cookie))
            user = model.get_user_by_id(user_id)
            self.logout(user)
            self.redirect('/')
        except TypeError:
            self.logout()
            self.redirect('/')

class Edit(MainHandler):
    def get(self, page):
        if self.user:
            self.render('edit.html')
        else:
            self.write('Not logged in')

    def post(self, page):
        if self.user:    
            content = self.request.get('content')
            author = self.user.name
            model.new_page(author = author, page = page)
            self.redirect('%s' % page)
        else:
            self.write('Not Logged in')
        
class WikiPage(MainHandler):
    def get(self, page):
        pass

import webapp2
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/', Index),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/_edit' + PAGE_RE, Edit),
                               (PAGE_RE, WikiPage)
                                ], 
                                 debug = True)
