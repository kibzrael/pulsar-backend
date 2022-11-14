from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

from posts.models import Post, Like
from users.models import User, MinimalUserSerializer

from pulsar.decorators.jwt_required import jwt_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class LikesView(View):
    # get likes of a certain post
    @jwt_required()
    def get(self, request, post_id, **kwargs):
        limit = int(request.GET.get("limit", 18))
        offset = int(request.GET.get("offset", 0)) * limit

        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The post you've entered does not exist."}
            )

        likes_query = User.objects.filter(post_liker__post__id=post_id)[
            offset : limit + offset
        ]
        likes = []
        for like in likes_query:
            likes.append(
                MinimalUserSerializer(instance=like).data,
                context={"request_user_id": kwargs.get("request_user")},
            )
        return JsonResponse(status=200, data={"likes": likes})

    # like a certain post
    @jwt_required()
    def post(self, request, post_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=request_user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The post you've entered does not exist."}
            )

        try:
            Like.objects.filter(user=user, post=post).get()
        except ObjectDoesNotExist:
            like = Like(user=user, post=post)
            like.save()

            return JsonResponse(
                status=200, data={"message": "You have successfully liked the post"}
            )
        else:
            return JsonResponse(
                status=200, data={"message": "You have already liked the post"}
            )

    # unlike a certain post
    @jwt_required()
    def delete(self, request, post_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=request_user_id)

            if post.user.id != request_user_id:
                return JsonResponse(
                    status=403,
                    data={"message": "You are not authorized to access this endpoint"},
                )
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The post you've entered does not exist."}
            )

        try:
            like = Like.objects.filter(user=user, post=post).get()
            like.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "You have not liked this post"}
            )

        return JsonResponse(
            status=200, data={"message": "You have successfully unliked this post"}
        )
