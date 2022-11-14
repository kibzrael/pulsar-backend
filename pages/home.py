from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from posts.models import Post
from posts.serializers import PostSerializer
from users.models import User
from pulsar.decorators.jwt_required import jwt_required


@jwt_required()
def home(request, **kwargs):
    request_user_id = kwargs.get("request_user")

    limit = int(request.GET.get("limit", 12))
    offset = int(request.GET.get("offset", 0)) * limit

    try:
        request_user = User.objects.get(id=request_user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404, data={"message": "The user you've entered does not exist"}
        )

    # posts from people following
    posts_query = Post.objects.filter(user__followedId__follower=request_user)[
        offset : limit + offset
    ]

    posts = []

    for post in posts_query:
        posts.append(
            PostSerializer(
                instance=post, context={"request_user_id": request_user_id}
            ).data
        )

    return JsonResponse(status=200, data={"posts": posts})
