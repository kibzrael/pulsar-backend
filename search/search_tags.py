from django.http.response import JsonResponse
from posts.models import Tag
from pulsar.decorators.jwt_required import jwt_required
import re


@jwt_required()
def search_tags(request, **kwargs):
    keyword = request.GET.get("keyword")
    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    if not keyword:
        return JsonResponse(status=411, data={"message": "Please provide a keyword"})

    regex = r"(?:{})".format(keyword)

    users_query = Tag.objects.filter(tag__iregex=regex).distinct("tag")[
        offset : limit + offset
    ]

    results = sorted(
        users_query,
        key=lambda e: len(e.tag)
        - (len(keyword) * len(re.findall(regex, e.tag, re.IGNORECASE))),
        reverse=False,
    )

    tags = []

    for tag in results:
        tags.append({"tag": tag.tag})

    return JsonResponse(status=200, data={"results": tags})
