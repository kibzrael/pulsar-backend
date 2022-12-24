from challenges.models import Challenge
from posts.models import Post
from posts.serializers import PostSerializer, points_calculation
from pulsar.decorators.jwt_required import jwt_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse


@jwt_required()
def leaderboard(request, challenge_id, *args, **kwargs):
    request_user_id = kwargs.get("request_user")

    limit = int(request.GET.get("limit", 20))
    offset = int(request.GET.get("offset", 0)) * limit

    try:
        challenge = Challenge.objects.get(id=challenge_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404,
            data={"message": "The challenge you've entered does not exist."},
        )

    points_queryset = Post.objects.filter(challenge=challenge).annotate(
        points=points_calculation
    )

    try:
        user_post = points_queryset.values().get(user__id=request_user_id)
        points = user_post.get("points")
        rank = points_queryset.filter(points__gte=points).count()
    except ObjectDoesNotExist:
        rank = 0
        points = 0

    results = points_queryset.order_by("-points")[offset : offset + limit]

    data = []
    for post in results:
        post_data = PostSerializer(
            instance=post,
        ).data
        data.append(post_data)

    return JsonResponse(
        status=200, data={"you": {"rank": rank, "points": points}, "data": data}
    )
