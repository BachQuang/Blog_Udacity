from google.appengine.ext import db
from controllers.control import BlogHandler
from support import blog_key

class EditPost(BlogHandler):
    def get(self, post_id):
        # Get logged in user
        user = self.validate_user("/signup-form.html")
        username = user.name

        # Get post by post_id
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        # Get post.owner
        owner = post.owner
        if owner != username:
            self.render("error.html", error="you cannot edit this post")
            return

        if not post:
            self.error(404)
            return
        self.render(
            'edit-post.html',
            subject=post.subject,
            content=post.content,
            error="")

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        post.subject = self.request.get('subject')
        post.content = self.request.get('content')
        post.put()

        self.redirect("/blog/" + post_id)
