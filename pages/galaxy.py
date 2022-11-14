from django.core.exceptions import ObjectDoesNotExist
from users.models import User
from pulsar.decorators.jwt_required import jwt_required
from django.http.response import JsonResponse

from pages.querysets import (
    discover_challenges,
    new_challenge_highlight,
    pinned_challenges,
    top_challenges,
)


@jwt_required()
def galaxy(request, **kwargs):
    request_user_id = kwargs.get("request_user")

    try:
        user = User.objects.get(id=request_user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=404, data={"message": "The user you've entered does not exist"}
        )

    pinned = pinned_challenges(user)
    trending = top_challenges(user)
    new_highlight = new_challenge_highlight(user)
    discover = discover_challenges(user, "For you")

    return JsonResponse(
        status=200,
        data={
            "pinned": pinned,
            "top": trending,
            "new highlight": new_highlight,
            "discover": discover,
        },
    )
