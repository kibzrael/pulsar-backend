from typing import List
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.db.models.query_utils import Q
from users.models import User
from users.serializers import MinimalUserSerializer
from pulsar.decorators.jwt_required import jwt_required
from users.interests import get_interests


@jwt_required()
def discover_users(request, **kwargs):
    limit = int(request.GET.get("limit", 12))
    offset = int(request.GET.get("offset", 0)) * limit

    request_user_id = kwargs.get("request_user")

    try:
        request_user = User.objects.get(id=request_user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=403,
            data={"message": "You are not authorized to access this endpoint"},
        )

    interests: List = get_interests(request_user)

    interests_id = list(map(lambda x: x["id"], interests))

    # same category or category in user's interests
    users_query = (
        User.objects.filter(
            Q(category=request_user.category)
            | Q(category__parent=request_user.category)
            | Q(category__subcategoryId=request_user.category)
            | Q(interest__category=request_user.category)
            | Q(interest__category__parent=request_user.category)
            | Q(interest__category__subcategoryId=request_user.category)
            | Q(category__in=interests_id)
            | Q(category__parent__in=interests_id)
            | Q(category__subcategoryId__in=interests_id)
            | Q(interest__category__in=interests_id)
            | Q(interest__category__parent__in=interests_id)
            | Q(interest__category__subcategoryId__in=interests_id)
        )
        .exclude(Q(id=request_user.id) | Q(followedId__follower__id=request_user.id))
        .distinct("id")[offset : limit + offset]
    )

    users = []

    for user in users_query:
        users.append(
            MinimalUserSerializer(
                instance=user, context={"request_user_id": request_user_id}
            ).data
        )
        # add cover from top video

    return JsonResponse(status=200, data={"users": users})
