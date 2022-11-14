from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

from users.models import PostNotification, User
from users.serializers import MinimalUserSerializer
from pulsar.decorators.jwt_required import jwt_required


class PostNotificationView(View):
    # get tracked users of a certain user
    @jwt_required()
    def get(self, request, user_id, **kwargs):
        limit = int(request.GET.get("limit", 18))
        offset = int(request.GET.get("offset", 0)) * limit

        request_user = kwargs.get("request_user")
        if user_id != request_user:
            return JsonResponse(
                status=404,
                data={"message": "You are not authorized to access this endpoint."},
            )

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The user you've entered does not exist."}
            )

        tracked_query = User.objects.filter(trackedId__notify=user)[
            offset : limit + offset
        ]
        tracked = []
        for tracked_user in tracked_query:
            tracked.append(
                MinimalUserSerializer(
                    instance=tracked_user, context={"request_user_id": request_user}
                ).data
            )
        return JsonResponse(status=200, data={"data": tracked})

    # track a certain user
    @jwt_required()
    def user(self, request, user_id, **kwargs):
        request_user_id = kwargs.get("request_user")
        if user_id == request_user_id:
            return JsonResponse(
                status=401, data={"message": "Invalid. You cannot track yourself"}
            )

        try:
            user = User.objects.get(id=user_id)
            request_user = User.objects.get(id=request_user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The user you're trying to track does not exist."},
            )

        try:
            PostNotification.objects.filter(user=user, notify=request_user).get()
        except ObjectDoesNotExist:
            notification = PostNotification(user=user, notify=request_user)
            notification.save()

            return JsonResponse(
                status=200,
                data={"message": f"You are successfully tracking @{user.username}"},
            )
        else:
            return JsonResponse(
                status=200, data={"message": "You are already tracking this user"}
            )

    # untrack a certain user
    @jwt_required()
    def delete(self, request, user_id, **kwargs):
        request_user_id = kwargs.get("request_user")
        try:
            user = User.objects.get(id=user_id)
            request_user = User.objects.get(id=request_user_id)

        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The user you're trying to untrack does not exist."},
            )

        try:
            notification = PostNotification.objects.filter(
                user=user, notify=request_user
            ).get()
            notification.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": f"You are not tracking @{user.username}"}
            )
        return JsonResponse(
            status=200,
            data={"message": f"You have successfully untracked @{user.username}"},
        )
