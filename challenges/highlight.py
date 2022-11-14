from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from users.models import User
from pulsar.decorators.jwt_required import jwt_required
from pages.querysets import new_challenge_highlight


@jwt_required()
def challenge_highlight(request, **kwargs):
    request_user_id = kwargs.get("request_user")

    try:
        request_user = User.objects.get(id=request_user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=403,
            data={"message": "You are not authorized to access this endpoint"},
        )

    challenge = new_challenge_highlight(request_user)

    return JsonResponse(status=200, data={"challenge": challenge})
