from controllers.control import BlogHandler
from models.user import User

from support import valid_username, valid_email, valid_password

#This document includes LogIn, LougOut, SignUp

class LogIn(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)


class LogOut(BlogHandler):

    def get(self):
        self.logout()
        self.redirect('/blog')


class SignUp(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        is_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        params = dict(username=username,
                      email=email)
        if not valid_username(username):
            params['error_username'] = "This username is not true"
            is_error = True
        if not valid_password(password):
            params['error_password'] = "This password is not true"
            is_error = True
        elif password != verify:
            params['error_verify'] = "It is not true"
            is_error = True
        if not valid_email(email):
            params['error_email'] = "This email is not true"
            is_error = True

        if is_error:
            self.render('signup-form.html', **params)
        else:
            u = User.get_by_name(username)
            if u:
                msg = 'That user already exists.'
                self.render('signup-form.html', error_username=msg)
            else:
                u = User.register(username, password, email)
                u.put()

                self.login(u)
                self.redirect('/blog')
