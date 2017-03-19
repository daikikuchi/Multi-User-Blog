from mainhandler import MainHandler
from models.blog import BlogPost
from google.appengine.ext import ndb


class PostPage(MainHandler):
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post, user=self.user)
