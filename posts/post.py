from posts.models import Post
from posts.serializers import PostSerializer
from pulsar.decorators.jwt_required import jwt_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class PostView(View):
    @jwt_required()
    def get(self, request, post_id, **kwargs):
        fields = request.GET.get("fields", "").split(",")
        if "" in fields:
            fields.remove("")
        try:
            post = Post.objects.get(id=post_id)
            post_serializer = PostSerializer(
                instance=post, context={"request_user_id": kwargs.get("request_user")}
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={
                    "message": "The post you've provided does not exist. Please try a valid post"
                },
            )
        return JsonResponse(
            status=200,
            data={
                "post": post_serializer.data,
            },
        )

    @jwt_required()
    def post(self, request, post_id, **kwargs):
        request_user = kwargs["request_user"]
        try:
            post: Post = Post.objects.get(id=post_id)
            user_id = post.user.id
            if user_id != request_user:
                return JsonResponse(
                    status=403,
                    data={
                        "message": "You are not authorized to perform this operation"
                    },
                )
            caption = request.POST.get("caption", post.caption)

            Post.objects.filter(id=post_id).update(caption=caption)

            #
            #
        #               remove current tags and save new tags from the caption -- And mentions ** where comment = null
        #
        #

        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={
                    "message": "The post you've provided does not exist. Please try a valid post"
                },
            )

        post = Post.objects.get(id=post_id)
        post_info = PostSerializer(
            instance=post, context={"request_user_id": request_user}
        ).data

        return JsonResponse(status=200, data={"post": post_info})

    @jwt_required()
    def delete(self, request, post_id, **kwargs):
        request_user = kwargs["request_user"]

        try:
            post = Post.objects.values().get(id=post_id)
            if post.get("user_id") != request_user:
                return JsonResponse(
                    status=403,
                    data={
                        "message": "You are not authorized to perform this operation"
                    },
                )
            post: Post = Post.objects.get(id=post_id)

        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={
                    "message": "The post you've provided does not exist. Please try a valid post"
                },
            )
        post.delete()

        return JsonResponse(
            status=200, data={"message": "The post has been deleted successfully"}
        )
