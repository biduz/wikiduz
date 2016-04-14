from main_handler import MainHandler
import model
import stuff

class Index(MainHandler):
    def get(self):
        self.render('index.html')

class Signup(MainHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        error, params = stuff.valid_signup(username, password, verify, email)
        if error:
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
        error, params, user =  stuff.valid_login(username, password)
        if not error:
            self.login(user)
            self.redirect('/')   
        else:
            self.render('login.html', **params)

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
    def get(self, path):
        if self.user:
            page = model.get_page(path)
            content = page.content if page else ' '
            self.render('edit.html', content = content)
        else:
            self.write('Not logged in')

    def post(self, path):
        if self.user:
            page = model.get_page(path)
            content = self.request.get('content')
            if not page:
                author = self.user.name
                model.new_page(author = author, path = path, content = content)
            else:
                editor = self.user.name
                model.edit_page(path = path, editor = editor, content = content)
            self.redirect('%s' % path)
        else:
            self.write('Not Logged in')
        
class WikiPage(MainHandler):
    def get(self, path):
        page = model.get_page(path)
        if page:
            page_content = stuff.escape_html(page.content)
            self.render('wikipage.html', page_content = page_content)
        else:
            self.redirect('/_edit%s' % path)

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
