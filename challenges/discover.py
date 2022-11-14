from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.db.models.query_utils import Q
from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer
from users.models import User
from pulsar.decorators.jwt_required import jwt_required
from pages.querysets import discover_challenges


@jwt_required()
def discover_challenges_view(request, **kwargs):
    # For you - user's category + user's interests ORDER BY not pinned
    tag = request.GET.get("tag", "For you")
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

    challenges = discover_challenges(request_user, tag=tag, offset=offset, limit=limit)

    return JsonResponse(status=200, data={"challenges": challenges})
