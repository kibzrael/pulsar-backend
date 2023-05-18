from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.db.models import Count
from challenges.models import Challenge
from posts.models import Post
from posts.serializers import PostSerializer, points_calculation
from pulsar.decorators.jwt_required import jwt_required


@jwt_required()
def challenge_posts(request, challenge_id, **kwargs):
    if request.method != "GET":
        return JsonResponse(
            status=405, data={"message": "The method you're using is invalid"}
        )

    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    index = int(request.GET.get("index", 0))

    try:
        challenge = Challenge.objects.get(id=challenge_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404, data={"message": "The challenge you've entered does not exist"}
        )

    posts_query = (
        Post.objects.filter(challenge=challenge).order_by("-time")[
            offset : limit + offset
        ]
        if index == 0
        else Post.objects.annotate(
            engagement=Count("post_like", distinct=True)
            + Count("post_comment", distinct=True)
            + Count("post_repost", distinct=True)
        )
        .filter(challenge=challenge)
        .order_by("-engagement")[offset : limit + offset]
    )
    posts = []

    for post in posts_query:
        posts.append(
            PostSerializer(
                instance=post, context={"request_user_id": kwargs.get("request_user")}
            ).data
        )

    return JsonResponse(status=200, data={"posts": posts})
