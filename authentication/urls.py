from django.urls import path

from authentication.login import log_in
from authentication.signup import sign_up
from authentication import google, facebook
from authentication.change_username import change_username
from authentication.change_password import change_password
from authentication.recover_account import recover_account
from authentication.reset_password import reset_password

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
    path("change_password", change_password, name="change_password"),
    path("recover_account", recover_account),
    path("reset_password", reset_password),
]
