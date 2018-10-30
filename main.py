import webapp2

# Controls
from controllers.control import BlogHandler
from controllers.blogfront import BlogFront
from controllers.login import LogIn, SignUp, LogOut
from controllers.post import PostPage, DeletePost, EditPost, Like, NewPost, Unlike 
from controllers.comment import AddComment, DeleteComment, EditComment


app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/([0-9]+)/comment/new', AddComment),
                               ('/blog/([0-9]+)/comment/edit/([0-9]+)', EditComment),
                               ('/blog/([0-9]+)/comment/delete/([0-9]+)', DeleteComment),
                               ('/blog/newpost', NewPost),
                               ('/blog/edit/([0-9]+)', EditPost),
                               ('/blog/delete/([0-9]+)', DeletePost),
                               ('/blog/like/([0-9]+)', Like),
                               ('/blog/unlike/([0-9]+)', Unlike),
                               ('/signup', SignUp),
                               ('/login', LogIn),
                               ('/logout', LogOut),
                               ('/welcome', DeletePost),
                               ],
                              debug=True)
