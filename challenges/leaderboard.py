from challenges.models import Challenge
from posts.models import Post
from users.serializers import MinimalUserSerializer
from pulsar.decorators.jwt_required import jwt_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.db.models import F, Count


@jwt_required()
def leaderboard(request, challenge_id, *args, **kwargs):
    request_user_id = kwargs.get("request_user")

    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    try:
        challenge = Challenge.objects.get(id=challenge_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404,
            data={"message": "The challenge you've entered does not exist."},
        )

    try:
        user_post = (
            Post.objects.annotate(
                points=Count("post_like") * 5
                + Count("post_comment") * 10
                + Count("post_repost") * 20
            )
            .values()
            .get(challenge=challenge, user__id=request_user_id)
        )
        rank = (
            Post.objects.filter(challenge=challenge)
            .annotate(
                points=Count("post_like") * 5
                + Count("post_comment") * 10
                + Count("post_repost") * 20
            )
            .filter(points__gte=user_post.get("points"))
            .count()
        )
    except ObjectDoesNotExist:
        return JsonResponse(
            status=403,
            data={"message": "You are not a participant in this challenge."},
        )

    results = (
        Post.objects.filter(challenge=challenge)
        .annotate(
            points=Count("post_like") * 5
            + Count("post_comment") * 10
            + Count("post_repost") * 20
        )
        .order_by("points")[offset : offset + limit]
    )

    data = []
    for post in results:
        user_data = MinimalUserSerializer(instance=post.user).data
        data.append(user_data)

    return JsonResponse(status=200, data={"you": rank, "data": data})
