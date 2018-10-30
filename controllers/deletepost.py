import time
from google.appengine.ext import db
from controllers.control import BlogHandler
from support import blog_key

class DeletePost(BlogHandler):
    def get(self, post_id):
        # Get logged in user
        user = self.validate_user("/signup-form.html")
        username = user.name

        # Get post by post_id
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        owner = post.owner
        if owner != username:
            self.render("error.html", error="No, way")
            return

        if not post:
            self.error(404)
            return
        # Check  owner
        owner = post.owner
        self.render(
            'delete-post.html',
            content="Do you want to delete your post?",
            post_id=post_id)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        post.delete()
        time.sleep(0.3)
        self.redirect("/blog")
