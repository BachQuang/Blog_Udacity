from google.appengine.ext import db
from controllers.control import BlogHandler
from support import blog_key


class Like(BlogHandler):
    def get(self, post_id):
        # Get logged in user
        user = self.validate_user("/signup-form.html")
        username = user.name

        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        # Get post.owner
        owner = post.owner

        # Get post.likes
        likes = str(post.user_likes)
        unlikes = str(post.user_unlikes)

        # if False:
        if owner == username:
            self.render("error.html", error="you can't like")
            return
        # Check user against post.likes
        elif username in likes:
            True
        else:
            # Check user against post.likes
            if username in unlikes:
                unlikes = unlikes.replace("|%s" % username, "")

            # Add user to post.likes
            likes = "|" + username
            post.user_likes = post.user_likes + likes
            post.user_unlikes = unlikes
            #post.subject = "Changed man"
            post.put()
        self.redirect("/blog/" + post_id)
