from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from users.models import Block, User
from users.serializers import MinimalUserSerializer

from pulsar.decorators.jwt_required import jwt_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class BlockView(View):
    # get blocked users of a certain user
    @jwt_required()
    def get(self, request, user_id, **kwargs):
        request_user = kwargs.get("request_user")
        if user_id != request_user:
            return JsonResponse(
                status=403,
                data={"message": "You are not authorized to access this endpoint"},
            )

        limit = int(request.GET.get("limit", 18))
        offset = int(request.GET.get("offset", 0)) * limit

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The user you've entered does not exist."}
            )

        blocks_query = User.objects.filter(blockedId__blocking=user)[
            offset : limit + offset
        ]
        blocks = []
        for block in blocks_query:
            blocks.append(
                MinimalUserSerializer(
                    instance=block, context={"request_user_id": request_user}
                ).data
            )
        return JsonResponse(status=200, data={"data": blocks})

    # block a certain user
    @jwt_required()
    def post(self, request, *args, **kwargs):
        request_user_id = kwargs.get("request_user")
        user_id = request.GET.get("user")

        if user_id == request_user_id:
            return JsonResponse(
                status=401, data={"message": "Invalid. You cannot block yourself"}
            )

        try:
            user = User.objects.get(id=user_id)
            request_user = User.objects.get(id=request_user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The user you're trying to block does not exist."},
            )

        try:
            Block.objects.filter(user=user, blocking=request_user).get()
        except ObjectDoesNotExist:
            block = Block(user=user, blocking=request_user)
            block.save()

            return JsonResponse(
                status=200,
                data={"message": f"You have successfully blocked @{user.username}"},
            )
        else:
            return JsonResponse(
                status=200, data={"message": "You have already blocked this user"}
            )

    # unblock a certain user
    @jwt_required()
    def delete(self, request, *args, **kwargs):
        request_user_id = kwargs.get("request_user")
        user_id = request.GET.get("user")
        try:
            user = User.objects.get(id=user_id)
            request_user = User.objects.get(id=request_user_id)

        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The user you're trying to unblock does not exist."},
            )

        try:
            block = Block.objects.filter(user=user, blocking=request_user).get()
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": f"You have not blocked @{user.username}"}
            )
            block.delete()

        return JsonResponse(
            status=200,
            data={"message": f"You have successfully unblocked @{user.username}"},
        )
