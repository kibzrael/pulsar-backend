from django.http.response import JsonResponse
from django.db.models.query_utils import Q
from users.models import User
from users.serializers import UserSerializer
from pulsar.decorators.jwt_required import jwt_required


@jwt_required()
def search_user(request, **kwargs):
    keyword = request.GET.get("keyword")
    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    request_user = kwargs.get("request_user")

    words = keyword.split(" ")

    users_query = User.objects.filter(
        Q(username__contains=keyword)
        | Q(fullname__contains=keyword)
        | Q(bio__contains=keyword)
    ).exclude(id=request_user)[offset : limit + offset]

    users = []

    for user in users_query:
        users.append(
            UserSerializer(
                instance=user, context={"request_user_id": request_user}
            ).data
        )

    return JsonResponse(status=200, data={"results": users})
