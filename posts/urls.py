from django.urls import path

from posts.create_post import create_post
from posts.post import PostView
from posts.comment import CommentsView, CommentView, CommentLikeView
from posts.like import LikesView
from posts.repost import RepostsView


urlpatterns = [
    path("", create_post),
    path("<int:post_id>", PostView.as_view()),
    #
    path("<int:post_id>/comments", CommentsView.as_view()),
    path("<int:post_id>/comments/<int:comment_id>", CommentView.as_view()),
    path("<int:post_id>/comments/<int:comment_id>/likes", CommentLikeView.as_view()),
    #
    path("<int:post_id>/likes", LikesView.as_view()),
    path("<int:post_id>/reposts", RepostsView.as_view()),
]
