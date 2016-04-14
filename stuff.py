from passlib.hash import sha512_crypt
import session
import hmac
import hashlib
import re
import model

#Password stuff
def make_pw_hash(pw):
    return sha512_crypt.encrypt(pw)

def valid_pw(pw, h):
    return sha512_crypt.verify(pw, h)
# end password stuff

# Session stuff
def make_secure_val(val, token):
    secure_val = hmac.new(token, val, hashlib.sha256).hexdigest()
    return '%s|%s' % (val, secure_val)

def make_user_cookie(user_id):
    token = session.get_session_token(user_id)
    return make_secure_val(str(user_id), token)

def get_val_from_secure_val(secure_val):
    return secure_val.split('|')[0]

def check_secure_val(secure_val):
	val = get_val_from_secure_val(secure_val)
	token = session.get_session_token(int(val))
	return make_secure_val(val, token) == secure_val
# end session stuff

def escape_html(html):
    escaped = html.replace('<script>', '&lt;script&gt;')
    escaped = escaped.replace('</script>', '&lt;/script&gt;')
    return escaped

def valid_signup(username, password, verify, email):
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
    return have_error, params

def valid_username(username):
    return username and re.match('^[\S]+$', username)

def available_username(username):
    return not model.get_user_by_name(username)

def valid_password(password, verify):
    return password and password == verify

def valid_email(email):
    return not email or re.match('^[\S]+@[\S]+\.[\S]+$', email)

def valid_login(username, password):
    have_error = False
    params = {'username': username}
    user = model.get_user_by_name(username)
    if user:
        if valid_pw(password, user.password):
            return have_error, params, user
        else:
            have_error = True
            params['error'] = 'Invalid Password'
    else:
        have_error = True
        params['error'] = 'Invalid User'
    return have_error, params, user
