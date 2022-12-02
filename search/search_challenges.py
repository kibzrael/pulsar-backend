from django.http.response import JsonResponse
from django.db.models.query_utils import Q
from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer
from pulsar.decorators.jwt_required import jwt_required
import re


@jwt_required()
def search_challenge(request, **kwargs):
    keyword = request.GET.get("keyword")
    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    request_user = kwargs.get("request_user")

    if not keyword:
        return JsonResponse(status=411, data={"message": "Please provide a keyword"})

    words = keyword.split(" ")
    keywords_regex = "|".join(words)
    regex = r"(?:{})".format(keywords_regex)

    challenges_query = Challenge.objects.filter(
        Q(name__iregex=regex)
        | Q(description__iregex=regex)
        | Q(category__name__iregex=regex)
    )[offset : limit + offset]

    results = sorted(
        challenges_query,
        key=lambda e: len(re.findall(regex, e.name, re.IGNORECASE))
        + len(re.findall(regex, e.description, re.IGNORECASE))
        + len(re.findall(regex, e.category.name, re.IGNORECASE)),
        reverse=True,
    )

    challenges = []

    for challenge in results:
        challenges.append(
            ChallengeSerializer(
                instance=challenge, context={"request_user_id": request_user}
            ).data
        )

    return JsonResponse(status=200, data={"results": challenges})
