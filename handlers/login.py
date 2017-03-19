from mainhandler import MainHandler
from models.user import User


class Login(MainHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg, user=self.user)


class Logout(MainHandler):
    def get(self):
        self.logout()
        self.redirect('/login')
