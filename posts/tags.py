from django.http.response import JsonResponse
from posts.serializers import PostSerializer
from pulsar.decorators.jwt_required import jwt_required
from posts.models import Post


@jwt_required()
def tag_posts(request, tag, **kwargs):
    if request.method != "GET":
        return JsonResponse(
            status=405,
            data={"message": "The method you are trying to accessed is not allowed"},
        )
    if not tag:
        return JsonResponse(status=411, data={"message": "Please provide a tag"})

    limit = int(request.GET.get("limit", 18))
    offset = int(request.GET.get("offset", 0)) * limit

    posts_count = Post.objects.filter(tag__tag=tag).count()
    posts_query = Post.objects.filter(tag__tag=tag)[offset : limit + offset]

    posts = []

    for post in posts_query:
        posts.append(
            PostSerializer(
                instance=post, context={"request_user_id": kwargs.get("request_user")}
            ).data
        )

    return JsonResponse(
        status=200, data={"tag": tag, "count": posts_count, "posts": posts}
    )
