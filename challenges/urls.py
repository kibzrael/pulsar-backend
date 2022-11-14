from django.urls import path

from challenges.create_challenge import create_challenge
from challenges.posts import challenge_posts
from challenges.pin import PinView
from challenges.highlight import challenge_highlight
from challenges.chart import challenge_chart
from challenges.discover import discover_challenges_view
from challenges.pinned import pinned_challenges_view
from search.search_challenges import search_challenge


urlpatterns = [
    path("", create_challenge),
    path("<int:challenge_id>/pins", PinView.as_view()),
    path("<int:challenge_id>/posts", challenge_posts),
    path("search", search_challenge),
    path("highlight", challenge_highlight),
    path("pinned", pinned_challenges_view),
    path("discover", discover_challenges_view),
    path("chart", challenge_chart),
]
