from django.urls import path

from pages.home import home
from pages.discover_posts import discover_posts
from pages.discover_users import discover_users
from pages.galaxy import galaxy

urlpatterns = [
    path("home", home),
    path("discover_posts", discover_posts),
    path("discover_users", discover_users),
    path("galaxy", galaxy),
]
