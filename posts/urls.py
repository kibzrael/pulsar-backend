from django.urls import path

from posts.create_post import create_post
from posts.post import PostView
from posts.comment import CommentsView, CommentView, CommentLikeView
from posts.like import LikesView
from posts.repost import RepostsView
from posts.tags import tag_posts
from search.search_tags import search_tags


urlpatterns = [
    path("", create_post),
    path("tag/<str:tag>", tag_posts),
    path("tags/search", search_tags),
    path("<int:post_id>", PostView.as_view()),
    #
    path("<int:post_id>/comments", CommentsView.as_view()),
    path("<int:post_id>/comments/<int:comment_id>", CommentView.as_view()),
    path("<int:post_id>/comments/<int:comment_id>/likes", CommentLikeView.as_view()),
    #
    path("<int:post_id>/likes", LikesView.as_view()),
    path("<int:post_id>/reposts", RepostsView.as_view()),
]
