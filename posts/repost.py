from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.http.response import JsonResponse

from posts.models import Post, Repost
from users.activity import ActivityType, activity
from users.models import User
from users.serializers import MinimalUserSerializer

from pulsar.decorators.jwt_required import jwt_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class RepostsView(View):
    # get reposts of a certain post
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

        reposts_query = User.objects.filter(post_reposter__post__id=post_id)[
            offset : limit + offset
        ]
        reposts = []
        for repost in reposts_query:
            reposts.append(
                MinimalUserSerializer(
                    instance=repost,
                    context={"request_user_id": kwargs.get("request_user")},
                ).data,
            )
        return JsonResponse(status=200, data={"reposts": reposts})

    # repost a certain post
    @jwt_required()
    def post(self, request, post_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=request_user_id)

            if post.user.id == user.id:
                return JsonResponse(
                    status=422, data={"message": "You cannot repost your own post"}
                )

        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The post you've entered does not exist."}
            )

        try:
            Repost.objects.filter(user=user, post=post).get()
        except ObjectDoesNotExist:
            repost = Repost(user=user, post=post)
            repost.save()
            activity(post.user, ActivityType.repost, user, post)
            return JsonResponse(
                status=200, data={"message": "You have successfully reposted the post"}
            )
        else:
            return JsonResponse(
                status=200, data={"message": "You have already reposted the post"}
            )

    # unrepost a certain post
    @jwt_required()
    def delete(self, request, post_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=request_user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The post you've entered does not exist."}
            )

        try:
            repost = Repost.objects.filter(user=user, post=post).get()
            repost.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "You have not reposted this post"}
            )

        return JsonResponse(
            status=200, data={"message": "You have successfully unreposted this post"}
        )
