import falcon
from .views.user import UserSignup

app = application = falcon.App()

user_signup = UserSignup()
app.add_route("/signup", user_signup)
