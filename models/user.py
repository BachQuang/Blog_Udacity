from google.appengine.ext import db
from support import users_key, make_pw_hash, valid_pw

class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def give_by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def get_by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.get_by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
