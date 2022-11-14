from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from challenges.models import Challenge, Pin
from users.models import User
from users.serializers import MinimalUserSerializer

from pulsar.decorators.jwt_required import jwt_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class PinView(View):
    @jwt_required()
    def get(self, request, challenge_id, **kwargs):
        limit = int(request.GET.get("limit", 18))
        offset = int(request.GET.get("offset", 0)) * limit

        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The challenge you've entered does not exist."},
            )

        pins_query = User.objects.filter(pin__challenge=challenge)[
            offset : limit + offset
        ]
        pins = []
        for pin in pins_query:
            pins.append(
                MinimalUserSerializer(
                    instance=pin,
                    context={"request_user_id": kwargs.get("request_user")},
                ).data
            )
        return JsonResponse(status=200, data={"data": pins})

    @jwt_required()
    def post(self, request, challenge_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            challenge = Challenge.objects.get(id=challenge_id)
            request_user = User.objects.get(id=request_user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={
                    "message": "The challenge you're trying to follow does not exist."
                },
            )

        try:
            Pin.objects.filter(user=request_user, challenge=challenge).get()
        except ObjectDoesNotExist:
            pin = Pin(challenge=challenge, user=request_user)
            pin.save()

            return JsonResponse(
                status=200,
                data={"message": f"You have successfully pinned @{challenge.name}"},
            )
        else:
            return JsonResponse(
                status=200, data={"message": "You have already pinned this challenge"}
            )

    @jwt_required()
    def delete(self, request, challenge_id, **kwargs):
        request_user_id = kwargs.get("request_user")
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            request_user = User.objects.get(id=request_user_id)

        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={
                    "message": "The challenge you're trying to unpin does not exist."
                },
            )

        try:
            pin = Pin.objects.filter(challenge=challenge, user=request_user).get()
            pin.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": f"You have not pinned @{challenge.name}"}
            )
        return JsonResponse(
            status=200,
            data={"message": f"You have successfully unpinned @{challenge.name}"},
        )
