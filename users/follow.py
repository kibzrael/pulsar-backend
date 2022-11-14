from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from users.models import Follow, User
from users.serializers import MinimalUserSerializer

from pulsar.decorators.jwt_required import jwt_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class FollowView(View):

    # get followers of a certain user
    @jwt_required()
    def get(self, request, user_id, **kwargs):
        limit = int(request.GET.get("limit", 18))
        offset = int(request.GET.get("offset", 0)) * limit

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The user you've entered does not exist."}
            )

        followers_query = User.objects.filter(followerId__user=user)[
            offset : limit + offset
        ]
        followers = []
        for follower in followers_query:
            followers.append(
                MinimalUserSerializer(
                    instance=follower,
                    context={"request_user_id": kwargs.get("request_user")},
                ).data
            )
        return JsonResponse(status=200, data={"data": followers})

    # follow a certain user
    @jwt_required()
    def post(self, request, user_id, **kwargs):
        request_user_id = kwargs.get("request_user")
        if user_id == request_user_id:
            return JsonResponse(
                status=401, data={"message": "Invalid. You cannot follow yourself"}
            )

        try:
            user = User.objects.get(id=user_id)
            request_user = User.objects.get(id=request_user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The user you're trying to follow does not exist."},
            )

        try:
            Follow.objects.filter(user=user, follower=request_user).get()
        except ObjectDoesNotExist:
            follow = Follow(user=user, follower=request_user)
            follow.save()

            return JsonResponse(
                status=200,
                data={"message": f"You have successfully followed @{user.username}"},
            )
        else:
            return JsonResponse(
                status=200, data={"message": "You are already following this user"}
            )

    # unfollow a certain user
    @jwt_required()
    def delete(self, request, user_id, **kwargs):
        request_user_id = kwargs.get("request_user")
        try:
            user = User.objects.get(id=user_id)
            request_user = User.objects.get(id=request_user_id)

        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The user you're trying to unfollow does not exist."},
            )

        try:
            follow = Follow.objects.filter(user=user, follower=request_user).get()
            follow.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": f"You are not following @{user.username}"}
            )
        return JsonResponse(
            status=200,
            data={"message": f"You have successfully unfollowed @{user.username}"},
        )
