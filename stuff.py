from passlib.hash import sha512_crypt

#Password stuff
def make_pw_hash(pw):
    return sha512_crypt.encrypt(pw)

def valid_pw(pw, h):
    return sha512_crypt.verify(pw, h)