from mainhandler import MainHandler
from models.blog import BlogPost


class PostPage(MainHandler):
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post, user=self.user)
