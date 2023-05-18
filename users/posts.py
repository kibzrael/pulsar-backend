from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from posts.models import Post
from posts.serializers import PostSerializer
from users.models import User
from pulsar.decorators.jwt_required import jwt_required


@jwt_required()
def user_posts(request, user_id, **kwargs):
    if request.method != "GET":
        return JsonResponse(
            status=405, data={"message": "The method you're using is invalid"}
        )

    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    index = int(request.GET.get("index", 0))

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404, data={"message": "The user you've entered does not exist"}
        )

    if index == 0:
        # user posts
        posts_query = Post.objects.filter(user=user).order_by("-time")[
            offset : limit + offset
        ]
    else:
        # user reposts
        posts_query = Post.objects.filter(post_repost__user=user).order_by("-time")[
            offset : limit + offset
        ]
    posts = []

    for post in posts_query:
        posts.append(
            PostSerializer(
                instance=post, context={"request_user_id": kwargs.get("request_user")}
            ).data
        )

    return JsonResponse(status=200, data={"posts": posts})
