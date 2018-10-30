from google.appengine.ext import db
from support import comment_key, render_str
from post import Post


class Comment(db.Model):
    owner = db.StringProperty(required=False)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    post = db.ReferenceProperty(Post, collection_name='post_comments')

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        self.id = str(self.key().id())
        return render_str(
            "post.html",
            p=self,
            likes=self.user_likes,
            unlikes=self.user_unlikes)
    def render_properties(self):
        return ('owner=%s content=%s' % (self.owner, self.content))

    @classmethod
    def get_by_id(cls, uid):
        return Comment.get_by_id(uid, parent=comment_key())
