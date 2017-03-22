from mainhandler import MainHandler
from models.blog import BlogPost, Comment
import time


class NewPost(MainHandler):
    def get(self):
        if self.user:
            self.render("new-post.html", user=self.user)
        else:
            self.redirect("/login")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = BlogPost(subject=subject,
                            content=content, user_id=self.user.key.id())

            post.put()
            self.redirect('/blog/%s' % str(post.key.id()))
        else:
            error = "Please enter subject and content!"
            self.render("new-post.html", subject=subject, content=content,
                        error=error, user=self.user)


class EditPost(MainHandler):
    def get(self, post_id):

        if not self.user:
            self.redirect("/login")

        else:
            post = BlogPost.get_by_id(int(post_id))

            if not post:
                msg = 'The post does not exist'
                self.render('error.html', error=msg, user=self.user)
            else:
                # get user who created the post
                user_from_post = post.user_id
                # compare user id that created the post with the login user id
                if self.user.key.id() == user_from_post:
                    self.render("edit-post.html", p=post, user=self.user)
                else:
                    msg = 'You are not allowed to edit this post'
                    self.render('error.html', error=msg, user=self.user)

    def post(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        edit_subject = self.request.get('subject')
        edit_content = self.request.get('content')

        if edit_subject and edit_content:
            post.subject = edit_subject
            post.content = edit_content
            post.put()
            self.redirect('/blog/%s' % str(post.key.id()))
        else:
            error = "Please enter subject and content!"
            self.render("edit-post.html", subject=edit_subject,
                        content=edit_content,
                        error=error, user=self.user, p=post)


class DeletePost(MainHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect("/login")
        else:
            post = BlogPost.get_by_id(int(post_id))
            if not post:
                # self.error(404)
                # return
                msg = 'The post does not exist'
                self.render('error.html', error=msg, user=self.user)
            else:
                # compare user id that created the post with the login user id
                if self.user.key.id() == post.user_id:
                    post.key.delete()
                    """ sleep 1s for google datastore to be updated, otherwise
                    deleted data still show up """
                    time.sleep(1)
                    """ delete all comments from the post also """
                    comments = Comment.query(ancestor=post.key).order(
                        -Comment.created).fetch()
                    if comments:
                        """ start deleting if there is comment """
                        for c in comments:
                            c.key.delete()
                    self.redirect('/blog')
                else:
                    msg = 'You are not allowed to delete this post'
                    self.render('error.html', error=msg, user=self.user)


class LikePost(MainHandler):
    def get(self, post_id):
        """ checking whether user is login, if not, redirect to login page """
        if self.user:
            post = BlogPost.get_by_id(int(post_id))
            user_id = post.user_id
            post.like += 1

            if not post:
                msg = 'The post does not exist'
                self.render('error.html', error=msg, user=self.user)
            # to check if the user of a post is different from login user
            else:
                if not (self.user.key.id() == user_id):
                    if post.liked_by:
                        # check if the user has already liked the post
                        if post.liked_by.find(self.user.name) == -1:
                            # not liked it yet
                            post.liked_by = "%s,%s" % (
                                post.liked_by, self.user.name)
                            post.put()
                            self.rebder('permalink.html', post=post,
                                        user=self.user)
                        else:
                            error = "You've already liked this post"
                            self.render('error.html', error=error,
                                        user=self.user)
                    else:  # you are the first person to like the post
                        post.liked_by = self.user.name
                        post.put()
                        self.render('permalink.html', post=post,
                                    user=self.user)
                else:
                    error = 'You are not allowed to like your own post'
                    self.render('error.html', error=error, user=self.user)
        else:
            self.redirect("/login")


class UnlikePost(MainHandler):
    def get(self, post_id):
        """ checking whether user is login, if not, redirect to login page """
        if self.user:
            post = BlogPost.get_by_id(int(post_id))
            user_id = post.user_id

            if not post:
                msg = 'The post does not exist'
                self.render('error.html', post_404=msg, user=self.user)
            else:
                if not (self.user.key.id() == user_id):
                    """ if the user has never liked the post before or
                    no one has liked it before """
                    if post.liked_by.find(self.user.name) == -1 \
                            or post.like == 0:
                        error = "you can not unlike the post"
                        self.render('error.html', error=error,
                                    user=self.user)
                    else:
                        post.like -= 1
                        print str(post.like)
                        post.liked_by = \
                            post.liked_by.replace(self.user.name, "")
                        post.put()
                        self.render('permalink.html',
                                    post=post, user=self.user)
                else:
                    error = 'You are not allowed to Unlike your own post'
                    self.render('error.html', error=error, user=self.user)
        else:
            self.redirect("/login")


class CommentPost(MainHandler):
    def get(self, post_id):
        if self.user:
            post = BlogPost.get_by_id(int(post_id))
            if not post:
                msg = 'The post does not exist'
                self.render('error.html', error=msg, user=self.user)
            else:
                """ get all comments from the same post id """
                comments = Comment.query(ancestor=post.key).order(
                    -Comment.created).fetch()
                self.render("comment.html", p=post, comments=comments,
                            user=self.user)
        else:
            self.redirect("/login")

    def post(self, post_id):
        comment = self.request.get('comment')
        if comment:
            post = BlogPost.get_by_id(int(post_id))
            if not post:
                msg = 'The post does not exist'
                self.render('error.html', error=msg, user=self.user)
            else:
                """ use post.key as the parent of the Comment instance """
                c = Comment(parent=post.key, comment=comment,
                            commented_by=self.user.name,
                            commented_by_ukey=self.user.key)
                c.put()

                # sleep 1s to make database updated
                time.sleep(1)
                """ get all comments from db again to display """
                comments = Comment.query(ancestor=post.key).order(
                    -Comment.created).fetch()
                self.render("comment.html", p=post, comments=comments,
                            user=self.user)
        else:
            msg = "Please enter a comment!"
            self.render('error.html', error_comment=msg, post_id=post_id,
                        user=self.user)


class DeleteComment(MainHandler):
    print("go to delete comment")
    """ deletion of comments"""

    def get(self, post_id, comment_id):
        post = BlogPost.get_by_id(int(post_id))
        if not post:
            msg = 'The post does not exist'
            self.render('error.html', error=msg, user=self.user)
        else:
            comment = Comment.get_by_id(int(comment_id), post.key)
            if self.user.key.id() == comment.commented_by_ukey.id():
                comment.key.delete()
                # sleep 1s to make database updated
                time.sleep(1)
                """ get all comments from db again to display """
                comments = Comment.query(ancestor=post.key).order(
                    -Comment.created).fetch()
                self.render("comment.html", p=post, comments=comments,
                            user=self.user)
            else:
                msg = 'You are not allowed to delete this comment'
                self.render('error.html', error=msg, user=self.user)


class EditComment(MainHandler):
    def post(self, post_id, comment_id):
        post = BlogPost.get_by_id(int(post_id))
        comment = Comment.get_by_id(int(comment_id), post.key)
        c = self.request.get('edit-comment-txt')
        print("comment from post " + c)
        if c:
            comment.comment = c
            comment.put()
            # sleep 1s to make database updated
            time.sleep(1)
            """ get all comments from db again to display """
            comments = Comment.query(ancestor=post.key).order(
                -Comment.created).fetch()
            self.render("comment.html", p=post, comments=comments,
                        user=self.user)
        else:
            error = "Please enter comment!"
            self.render("error.html",
                        error_comment=error, user=self.user,
                        comment_id=comment_id, post_id=post_id)
