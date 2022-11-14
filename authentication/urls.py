from django.urls import path

from authentication.login import log_in

urlpatterns = [
    path("login", log_in),
]
