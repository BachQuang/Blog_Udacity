import time
from google.appengine.ext import db
from controllers.control import BlogHandler
from models.comment import Comment


class DeleteComment(BlogHandler):
    def get(self, post_id, comment_id):
        # Get logged in user
        user = self.validate_user("/signup-form.html")
        username = user.name

        # Get post.owner
        comment = Comment.get_by_id(int(comment_id))
        owner = comment.owner

        if owner != username:
            self.render("error.html", error="you can't delete this comment")
            return

        if not comment:
            self.error(404)
            return
        comment.delete()
        time.sleep(0.2)
        self.redirect('/blog')
