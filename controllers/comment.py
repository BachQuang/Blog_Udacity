import time
from google.appengine.ext import db

from models.comment import Comment
from controllers.control import BlogHandler

from support import blog_key, comment_key
# This document includes AddComment, DeleteComment and EditComment

class AddComment(BlogHandler):
    def post(self, post_id):
        user = self.validate_user("/signup-form.html")
        if user:
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


class DeleteComment(BlogHandler):
    def get(self, post_id, comment_id):
        # Get logged in user
        user = self.validate_user("/signup-form.html")
        if user:
            username = user.name

            # Get post.owner
            comment = Comment.capture_by_id(int(comment_id))
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


class EditComment(BlogHandler):
    def get(self, post_id, comment_id):
        # Get logged in user
        user = self.validate_user("/signup-form.html")
        if user:
            username = user.name

            # Get post.owner
            comment = Comment.capture_by_id(int(comment_id))
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
        if user:
            comment = Comment.capture_by_id(int(comment_id))
            content = self.request.get('content')
            comment.content = content
            comment.put()
            time.sleep(0.1)
            self.redirect('/blog')
