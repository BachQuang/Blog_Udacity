from google.appengine.ext import db
from controllers.control import BlogHandler


class BlogFront(BlogHandler):
    def get(self):
        posts = db.GqlQuery(
            "select * from Post order by created desc limit 10")

        self.render('front.html', posts=posts)
