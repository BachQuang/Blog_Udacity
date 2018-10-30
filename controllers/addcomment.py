import time
from google.appengine.ext import db
from controllers.control import BlogHandler
from models.comment import Comment
from support import blog_key, comment_key

class AddComment(BlogHandler):
    def post(self, post_id):
        user = self.validate_user("/signup-form.html")
        username = user.name

        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        content = self.request.get('content')
        if content:
            comment = Comment(parent=comment_key(), owner=username,
                              content=content, post=post)
            comment.put()
        time.sleep(0.1)
        self.redirect('/blog')
