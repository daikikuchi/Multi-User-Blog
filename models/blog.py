import os
import jinja2
from user import User
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


# BlogPost entity in ndb to store information relating to post
class BlogPost(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    like = ndb.IntegerProperty(default=0)
    liked_by = ndb.StringProperty()
    last_modified = ndb.DateTimeProperty(auto_now=True)
    # user id of the user who creates the post
    user_id = ndb.IntegerProperty(required=True)

    # to get all comments from a BlogPost instance key
    @classmethod
    def get_comments(cls):
        cls.comments = Comment.query(ancestor=cls.key).order(
            -Comment.created).fetch()
        return cls.comments

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        """ count the number of comments to display on html page """
        n = Comment.query(ancestor=self.key).count()
        print("no of comments " + str(n))
        return render_str("post.html", p=self, noComments=n)


# Comment entity in ndb to store comment related information, Comment's parent
# is BlogPost
class Comment(ndb.Model):
    comment = ndb.TextProperty()
    commented_by = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
