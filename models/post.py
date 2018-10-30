from google.appengine.ext import db
from support import render_str

class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modifed = db.DateTimeProperty(auto_now=True)
    user_likes = db.StringProperty()
    user_unlikes = db.StringProperty()
    owner = db.StringProperty(required=False)

    def render(self, link_to_self=False):
        self._render_text = self.content.replace('\n', '<br>')
        self.id = str(self.key().id())
        return render_str(
            "post.html",
            p=self,
            likes=len(
                self.user_likes.split("|")) -
            1 if self.user_likes else 0,
            unlikes=len(
                self.user_unlikes.split("|")) -
            1 if self.user_unlikes else 0,
            link_to_self=link_to_self)

    def render_properties(self):
        return ('subject=%s owner=%s content=%s user_likes=%s user_unlikes=%s' % (
            self.subject, self.owner, self.content, self.user_likes, self.user_unlikes))
