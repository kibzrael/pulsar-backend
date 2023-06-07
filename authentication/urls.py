from django.urls import path

from authentication import facebook, google
from authentication.change_email import change_email
from authentication.change_password import change_password
from authentication.change_username import change_username
from authentication.login import log_in
from authentication.recover_account import recover_account
from authentication.reset_password import reset_password
from authentication.signup import sign_up
from authentication.verify_email import verify_email

urlpatterns = [
    path("login", log_in),
    path("signup", sign_up),
    #
    path("google/signin", google.sign_in),
    path("google/signup", google.sign_up),
    #
    path("facebook/signin", facebook.sign_in),
    path("facebook/signup", facebook.sign_up),
    #
    path("change_username", change_username, name="change_username"),
    path("change_email", change_email, name="change_email"),
    path("change_password", change_password, name="change_password"),
    path("recover_account", recover_account),
    path("verify_email", verify_email),
    path("reset_password", reset_password),
]
