import time
from google.appengine.ext import db

from controllers.control import BlogHandler
from models.comment import Comment
from models.post import Post
from support import render_str

from support import blog_key, render_str

#This document includes PostPage, Newpost, DeletePost, EditPost, Like, Unlike.

class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return
        self.render("permalink.html", post=post)


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


class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            return self.redirect('/blog')

        subject = self.request.get('subject')
        username = self.user.name
        content = self.request.get('content')

        if subject and content:
            p = Post(
                parent=blog_key(),
                subject=subject,
                owner=username,
                user_likes="",
                user_unlikes="",
                content=content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render(
                "newpost.html",
                subject=subject,
                content=content,
                error=error)


class Unlike(BlogHandler):
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

        # Check user against owner
        # if False:
        if owner == username:
            self.render("error.html", error="you can't unlike")
            return
        # Check user against post.likes
        elif username in unlikes:
            False
        else:
            # Check user against post.likes
            if username in likes:
                likes = likes.replace("|%s" % username, "")

            # Add user to post.likes
            unlikes = "|" + username
            post.user_unlikes += unlikes
            post.user_likes = likes
            #post.subject = "Changed man"
            post.put()
        self.redirect("/blog/" + post_id)
