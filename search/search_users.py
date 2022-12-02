from django.http.response import JsonResponse
from django.db.models.query_utils import Q
from users.models import User
from users.serializers import UserSerializer
from pulsar.decorators.jwt_required import jwt_required
import re


@jwt_required()
def search_user(request, **kwargs):
    keyword = request.GET.get("keyword")
    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    request_user = kwargs.get("request_user")

    if not keyword:
        return JsonResponse(status=411, data={"message": "Please provide a keyword"})

    words = keyword.split(" ")
    keywords_regex = "|".join(words)
    regex = r"(?:{})".format(keywords_regex)

    users_query = User.objects.filter(
        Q(username__iregex=regex) | Q(fullname__iregex=regex) | Q(bio__iregex=regex)
    ).exclude(id=request_user)[offset : limit + offset]

    results = sorted(
        users_query,
        key=lambda e: len(re.findall(regex, e.username, re.IGNORECASE))
        + len(re.findall(regex, e.fullname, re.IGNORECASE))
        + len(re.findall(regex, e.bio if e.bio else "", re.IGNORECASE)),
        reverse=True,
    )

    users = []

    for user in results:
        users.append(
            UserSerializer(
                instance=user, context={"request_user_id": request_user}
            ).data
        )

    return JsonResponse(status=200, data={"results": users})
