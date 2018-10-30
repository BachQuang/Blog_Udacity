import time
from google.appengine.ext import db
from controllers.control import BlogHandler
from models.comment import Comment

class EditComment(BlogHandler):
    def get(self, post_id, comment_id):
        # Get logged in user
        user = self.validate_user("/signup-form.html")
        username = user.name

        # Get post.owner
        comment = Comment.get_by_id(int(comment_id))
        owner = comment.owner

        if owner != username:
            self.render("error.html", error="you cannot edit this comment")
            return

        if not comment:
            self.error(404)
            return

        self.render(
            'edit-post.html',
            content=comment.content,
            error="",
            comment=True)

    def post(self, post_id, comment_id):
        # Get logged in user
        user = self.validate_user("/signup-form.html")

        comment = Comment.get_by_id(int(comment_id))
        content = self.request.get('content')
        comment.content = content
        comment.put()
        time.sleep(0.1)
        self.redirect('/blog')
