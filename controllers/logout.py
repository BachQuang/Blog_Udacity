from controllers.control import BlogHandler


class LogOut(BlogHandler):

    def get(self):
        self.logout()
        self.redirect('/blog')
