import os
from support import *


# Models
from models.user import User
from models.post import Post
from models.comment import Comment

# Controls
from controllers.control import BlogHandler
from controllers.blogfront import BlogFront
from controllers.signup import SignUp
from controllers.login import LogIn
from controllers.logout import LogOut
from controllers.post import PostPage
from controllers.newpost import NewPost
from controllers.editpost import EditPost
from controllers.deletepost import DeletePost
from controllers.addcomment import AddComment
from controllers.editcomment import EditComment
from controllers.deletecomment import DeleteComment
from controllers.likepost import Like
from controllers.unlikepost import Unlike


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
