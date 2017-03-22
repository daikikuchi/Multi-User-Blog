import webapp2
from handlers.mainhandler import MainHandler
from models.blog import BlogPost
from handlers.postpage import PostPage

from handlers.login import Login, Logout
from handlers.bloghandler import NewPost, EditPost, DeletePost, \
    LikePost, UnlikePost, CommentPost, EditComment, DeleteComment
from handlers.userregister import UserRegister


# Main page displays all the posts
class MainPage(MainHandler):
    def get(self):
        posts = BlogPost.query().order(-BlogPost.created).fetch()
        self.render('base.html', posts=posts, user=self.user)


app = webapp2.WSGIApplication\
    ([('/', MainPage),
      ('/register', UserRegister),
      ('/login', Login),
      ('/logout', Logout),
      ('/blog/?', MainPage),
      ('/blog/([0-9]+)', PostPage),
      ('/blog/newpost', NewPost),
      ('/blog/([0-9]+)/edit', EditPost),
      ('/blog/([0-9]+)/delete', DeletePost),
      ('/blog/([0-9]+)/like', LikePost),
      ('/blog/([0-9]+)/unlike', UnlikePost),
      ('/blog/([0-9]+)/comment', CommentPost),
      ('/blog/([0-9]+)/([0-9]+)/edit', EditComment),
      ('/blog/([0-9]+)/([0-9]+)/delete', DeleteComment),
      ],
     debug=True)
