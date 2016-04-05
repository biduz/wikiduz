from passlib.hash import sha512_crypt
import session
import hmac
import hashlib

#Password stuff
def make_pw_hash(pw):
    return sha512_crypt.encrypt(pw)

def valid_pw(pw, h):
    return sha512_crypt.verify(pw, h)

# Session stuff
def make_secure_val(val, token):
    secure_val = hmac.new(token, val, hashlib.sha256).hexdigest()
    return '%s|%s' % (val, secure_val)

def make_user_cookie(user_id):
    token = session.get_session_token(user_id)
    return make_secure_val(str(user_id), token)
