from django.urls import path

from users.profile import Profile
from users.categories import create_category, get_categories
from users.posts import user_posts
from users.follow import FollowView
from users.block import BlockView
from users.notification import PostNotificationView
from search.search_users import search_user


urlpatterns = [
    path("<int:user_id>", Profile.as_view()),
    #
    path("create_category", create_category, name="create_category"),
    path("categories", get_categories),
    #
    path("<int:user_id>/posts", user_posts),
    path("<int:user_id>/followers", FollowView.as_view()),
    path("<int:user_id>/blocks", BlockView.as_view()),
    path("<int:user_id>/notifications", PostNotificationView.as_view()),
    path("search", search_user),
]
