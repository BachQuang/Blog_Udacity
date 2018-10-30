from controllers.control import BlogHandler
from models.comment import Comment
from models.post import Post
from support import blog_key

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
