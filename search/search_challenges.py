from django.http.response import JsonResponse
from django.db.models.query_utils import Q
from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer
from pulsar.decorators.jwt_required import jwt_required


@jwt_required()
def search_challenge(request, **kwargs):
    keyword = request.GET.get("keyword")
    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    request_user = kwargs.get("request_user")

    words = keyword.split(" ")

    challenges_query = Challenge.objects.filter(
        Q(name__contains=keyword)
        | Q(description__contains=keyword)
        | Q(category__name__contains=keyword)
    )[offset : limit + offset]

    challenges = []

    for challenge in challenges_query:
        challenges.append(
            ChallengeSerializer(
                instance=challenge, context={"request_user_id": request_user}
            ).data
        )

    return JsonResponse(status=200, data={"results": challenges})
